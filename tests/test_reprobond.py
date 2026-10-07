import copy
import hashlib
import json
import re
from pathlib import Path
import pytest

BASE = 'https://raw.githubusercontent.com/haris4587/ReproBond/' + 'a' * 40 + '/evidence/fixtures/'
PAPER = Path('evidence/fixtures/original.md').read_bytes()
REPORT = Path('evidence/fixtures/negative-replication.md').read_bytes()


def fp(name, body):
    return {'url': BASE + name, 'sha256': hashlib.sha256(body).hexdigest(), 'bytes': len(body)}


def make_terms():
    return {'title': 'Synthetic pendulum calibration', 'paper': fp('original.md', PAPER), 'hypothesis': 'Period 1.90..2.10s',
        'protocol': 'Three trials of ten oscillations', 'methodology': '1.00m, 5 degrees, manual stopwatch',
        'allowed_deviations': '1cm length uncertainty, manual stopwatch', 'disallowed_deviations': 'Different length or angle',
        'report_fields': 'apparatus, angle, durations, mean, deviations, conclusion, limitations',
        'minimum_evidence': 'Synthetic demonstration: one complete UTF-8 report with raw timings; no video required.'}


def result(outcome='FAILED_TO_REPLICATE'):
    return {'outcome': outcome, 'methodology_score': 95 if outcome in ('REPLICATED', 'FAILED_TO_REPLICATE') else 40,
        'material_deviations': [] if outcome != 'INVALID_REPLICATION' else ['Changed length'],
        'citations': [BASE + 'negative-replication.md'], 'evidence_quality_score': 90 if outcome != 'INCONCLUSIVE' else 30,
        'reasoning': 'Auditable fixture shows a completed comparable synthetic replication with mean period 2.30s.'}


@pytest.fixture
def env(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    vm = direct_vm
    vm.sender = direct_alice
    vm.warp('2026-10-07T00:00:00Z')
    vm.mock_web(re.escape(BASE + 'original.md'), {'status': 200, 'body': PAPER.decode()})
    vm.mock_web(re.escape(BASE + 'negative-replication.md'), {'status': 200, 'body': REPORT.decode()})
    vm.mock_llm('You are a scientific methodology reviewer', json.dumps(result()))
    vm.mock_llm('Compare these independently', 'YES')
    contract = direct_deploy('contracts/reprobond.py', sdk_version='v0.2.16')
    vm.value = 100
    bid = contract.create_bounty(json.dumps(make_terms()), 1791331800, 7, 2)
    vm.value = 0
    from genlayer import Address
    return vm, contract, bid, Address(direct_alice), Address(direct_bob), Address(direct_charlie)


def submit(env):
    vm, c, bid, sponsor, researcher, _ = env
    items = json.dumps([fp('negative-replication.md', REPORT)])
    vm.sender = sponsor
    c.authorize_package(bid, str(researcher), items)
    vm.sender = researcher
    vm.value = 7
    sid = c.submit(bid, items)
    vm.value = 0
    return sid, items


def state(env):
    return json.loads(env[1].get_bounty(env[2]))


def invariant(c):
    a = json.loads(c.get_accounting())
    assert a['deposited'] == a['escrow'] + a['credits'] + a['withdrawn']
    return a


def test_funded_creation(env):
    assert state(env)['reward'] == 100
    assert invariant(env[1]) == {'deposited': 100, 'escrow': 100, 'credits': 0, 'withdrawn': 0}


@pytest.mark.parametrize('value,deadline,cap', [(0,1791331800,2),(1,0,2),(1,9999999999,2),(1,1791331800,0),(1,1791331800,5)])
def test_bad_creation(env,value,deadline,cap):
    vm,c,*_ = env
    vm.value = value
    with pytest.raises(Exception):
        c.create_bounty(json.dumps(make_terms()),deadline,0,cap)
    assert invariant(c)['deposited'] == 100


def test_unknown_id(env):
    with pytest.raises(Exception):
        env[1].adjudicate_next(999)


def test_immutable_terms(env):
    before = state(env)['terms_hash']
    submit(env)
    env[1].adjudicate_next(env[2])
    assert state(env)['terms_hash'] == before
    assert not hasattr(env[1], 'update_terms')


def test_authorization_and_submitter_copy(env):
    vm,c,bid,sponsor,researcher,attacker = env
    items = json.dumps([fp('negative-replication.md',REPORT)])
    vm.sender = attacker
    with pytest.raises(Exception,match='sponsor only'):
        c.authorize_package(bid,str(attacker),items)
    vm.sender = sponsor
    c.authorize_package(bid,str(researcher),items)
    vm.sender = attacker
    vm.value = 7
    with pytest.raises(Exception,match='researcher only'):
        c.submit(bid,items)
    assert state(env)['submissions'] == []
    vm.sender = researcher
    c.submit(bid,items)
    vm.value = 0
    c.adjudicate_next(bid)
    assert c.get_credit(str(attacker)) == 0
    assert c.get_credit(str(researcher)) == 107


def test_duplicate_content_under_another_url_cannot_rebind(env):
    _,items = submit(env)
    vm,c,bid,sponsor,_,attacker = env
    vm.sender = sponsor
    altered = json.loads(items)
    altered[0]['url'] = BASE + 'copy.md'
    with pytest.raises(Exception,match='content already bound'):
        c.authorize_package(bid,str(attacker),json.dumps(altered))


def test_package_replay(env):
    _,items = submit(env)
    env[0].value = 7
    with pytest.raises(Exception,match='package replay'):
        env[1].submit(env[2],items)
    assert invariant(env[1])['deposited'] == 107


def test_unauthorized_package(env):
    env[0].value = 7
    with pytest.raises(Exception,match='not authorized'):
        env[1].submit(env[2],json.dumps([fp('negative-replication.md',REPORT)]))


@pytest.mark.parametrize('amount',[0,6,8])
def test_exact_bond(env,amount):
    _,items = submit(env)
    env[0].value = amount
    with pytest.raises(Exception,match='exact bond'):
        env[1].submit(env[2],items)


@pytest.mark.parametrize('outcome',['REPLICATED','FAILED_TO_REPLICATE','INVALID_REPLICATION','INCONCLUSIVE'])
def test_outcome_and_reward(env,outcome):
    submit(env)
    vm,c,bid,_,researcher,_ = env
    vm._llm_mocks = []
    vm.mock_llm('You are a scientific methodology reviewer',json.dumps(result(outcome)))
    vm.mock_llm('Compare these independently','YES')
    assert c.adjudicate_next(bid) == outcome
    b = state(env)
    assert b['status'] == ('AWARDED' if outcome in ('REPLICATED','FAILED_TO_REPLICATE') else 'OPEN')
    assert c.get_credit(str(researcher)) == (107 if b['status']=='AWARDED' else 7)
    assert len(b['submissions'][0]['decision_hash']) == 64
    invariant(c)


def test_double_settlement_and_final_immutability(env):
    submit(env)
    c,bid = env[1:3]
    c.adjudicate_next(bid)
    before = c.get_bounty(bid)
    for action in [lambda:c.adjudicate_next(bid),lambda:c.expire(bid),lambda:c.authorize_package(bid,str(env[4]),'[]')]:
        with pytest.raises(Exception): action()
    assert c.get_bounty(bid) == before
    invariant(c)


def test_refund_and_boundary(env):
    vm,c,bid,sponsor,*_ = env
    vm.warp('2026-10-07T00:10:00Z')
    with pytest.raises(Exception,match='too early'): c.expire(bid)
    vm.warp('2026-10-07T00:10:01Z')
    c.expire(bid)
    assert c.get_credit(str(sponsor)) == 100
    assert state(env)['status'] == 'REFUNDED'
    invariant(c)


def test_pending_escape_returns_all_bonds(env):
    submit(env)
    vm,c,bid,sponsor,researcher,_ = env
    vm.warp('2026-10-08T00:10:00Z')
    with pytest.raises(Exception): c.expire(bid)
    vm.warp('2026-10-08T00:10:01Z')
    c.expire(bid)
    assert c.get_credit(str(sponsor)) == 100
    assert c.get_credit(str(researcher)) == 7
    assert invariant(c)['escrow'] == 0


def test_no_submit_at_deadline(env):
    vm,c,bid,sponsor,researcher,_ = env
    items=json.dumps([fp('negative-replication.md',REPORT)])
    c.authorize_package(bid,str(researcher),items)
    vm.sender=researcher
    vm.value=7
    vm.warp('2026-10-07T00:10:00Z')
    with pytest.raises(Exception,match='closed'): c.submit(bid,items)


@pytest.mark.parametrize('url',[
    'http://raw.githubusercontent.com/a/b/'+'a'*40+'/f.md',
    'https://user:pass@raw.githubusercontent.com/a/b/'+'a'*40+'/f.md',
    BASE+'f.md#fragment', BASE+'f.md?query=1', BASE+'../f.md', BASE+'%2e/f.md', BASE+'//f.md',
    'https://127.0.0.1/file', 'https://raw.githubusercontent.com:443/a/b/'+'a'*40+'/f.md',
    'https://raw.githubusercontent.com/a/b/main/f.md','https://evil.example/file'])
def test_invalid_urls(env,url):
    item=fp('negative-replication.md',REPORT); item['url']=url
    with pytest.raises(Exception): env[1].authorize_package(env[2],str(env[4]),json.dumps([item]))


@pytest.mark.parametrize('items',[[],[fp('negative-replication.md',REPORT)]*3,[fp('negative-replication.md',REPORT)]*2])
def test_evidence_caps_duplicates(env,items):
    with pytest.raises(Exception): env[1].authorize_package(env[2],str(env[4]),json.dumps(items))


@pytest.mark.parametrize('fault',['hash','length','unavailable','oversize','encoding'])
def test_authentication_failures(env,fault):
    vm,c,bid,sponsor,researcher,_=env
    item=fp('negative-replication.md',REPORT)
    if fault=='hash': item['sha256']='0'*64
    if fault=='length': item['bytes']+=1
    if fault in ('unavailable','oversize','encoding'):
        vm._web_mocks=[]
        body=REPORT.decode() if fault=='unavailable' else ('X'*24001 if fault=='oversize' else b'\xff')
        vm.mock_web(re.escape(item['url']),{'status':404 if fault=='unavailable' else 200,'body':body})
    c.authorize_package(bid,str(researcher),json.dumps([item]))
    vm.sender=researcher;vm.value=7
    with pytest.raises(Exception,match='inaccessible or fingerprint'): c.submit(bid,json.dumps([item]))
    assert state(env)['submissions']==[]
    invariant(c)


def test_changed_after_submit_inconclusive(env):
    submit(env)
    vm,c,bid,_,researcher,_=env
    vm._web_mocks=[]
    vm.mock_web(re.escape(BASE+'original.md'),{'status':200,'body':PAPER.decode()})
    vm.mock_web(re.escape(BASE+'negative-replication.md'),{'status':200,'body':'changed'})
    assert c.adjudicate_next(bid)=='INCONCLUSIVE'
    assert c.get_credit(str(researcher))==7
    assert invariant(c)['escrow']==100


def test_validator_independent_refetch_and_forged_outcome(env):
    submit(env)
    vm,c,bid,*_=env
    c.adjudicate_next(bid)
    assert vm.run_validator(leader_result=result()) is True
    assert vm.run_validator(leader_result=result('REPLICATED')) is False
    vm._web_mocks=[]
    vm.mock_web('.*',{'status':404,'body':''})
    assert vm.run_validator(leader_result=result()) is False


@pytest.mark.parametrize('field,value',[('methodology_score',True),('evidence_quality_score',101),('outcome','PAY_ME'),
    ('citations',['https://evil.example']),('material_deviations',['Changed length']),('reasoning','')])
def test_malformed_or_ineligible_llm(env,field,value):
    submit(env)
    vm,c,bid,*_=env
    bad=result(); bad[field]=value
    vm._llm_mocks=[]
    vm.mock_llm('You are a scientific methodology reviewer',json.dumps(bad))
    with pytest.raises(Exception): c.adjudicate_next(bid)
    assert state(env)['submissions'][0]['verdict'] is None
    invariant(c)


def test_withdraw_emits_once(env):
    submit(env)
    vm,c,bid,_,researcher,_=env
    c.adjudicate_next(bid)
    vm.sender=researcher
    messages=[]
    def record(vm, request):
        if 'EthSend' in request:
            messages.append(request['EthSend'])
            return {'ok': None}
    vm._gl_call_hook=record
    assert c.withdraw()==107
    assert c.get_credit(str(researcher))==0
    with pytest.raises(Exception,match='no credit'): c.withdraw()
    assert invariant(c)['withdrawn']==107
    assert len(messages)==1
    assert messages[0]['value']==107
    assert str(messages[0]['address'])==str(researcher)
    assert messages[0]['calldata']==b''


def test_append_only_history_and_bounds(env):
    before=env[1].get_history(0,50)
    submit(env)
    after=env[1].get_history(0,50)
    assert after[:len(before)]==before and len(after)==3
    with pytest.raises(Exception): env[1].get_history(0,100)


def test_first_qualifying_in_submission_order(env):
    submit(env)
    vm,c,bid,sponsor,researcher,other=env
    second=REPORT+b'\nSecond independent authorized synthetic report.\n'
    items=json.dumps([fp('second.md',second)])
    vm.sender=sponsor
    c.authorize_package(bid,str(other),items)
    vm.mock_web(re.escape(BASE+'second.md'),{'status':200,'body':second.decode()})
    vm.sender=other;vm.value=7
    assert c.submit(bid,items)==1
    vm.value=0
    # Later submitter may trigger adjudication but cannot skip the first submission.
    c.adjudicate_next(bid)
    assert state(env)['winner']==0
    assert c.get_credit(str(researcher))==107
    assert c.get_credit(str(other))==7
    assert invariant(c)['escrow']==0


def test_authorization_limit_and_zero_address(env):
    vm,c,bid,sponsor,researcher,_=env
    with pytest.raises(Exception,match='zero researcher'):
        c.authorize_package(bid,'0x'+'0'*40,json.dumps([fp('negative-replication.md',REPORT)]))
    for i in range(8):
        c.authorize_package(bid,str(researcher),json.dumps([fp(f'report{i}.md',str(i).encode())]))
    with pytest.raises(Exception,match='authorization limit'):
        c.authorize_package(bid,str(researcher),json.dumps([fp('report9.md',b'9')]))


def test_decision_hash_binds_exact_inputs(env):
    submit(env)
    vm,c,bid,*_=env
    c.adjudicate_next(bid)
    b=state(env);s=b['submissions'][0]
    from genlayer import gl
    value={'chain':int(gl.message.chain_id),'contract':str(gl.message.contract_address),'bounty':int(bid),
        'terms_hash':b['terms_hash'],'submission':0,'researcher':s['researcher'],'package_hash':s['package_hash'],'result':s['verdict']}
    raw=json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()
    assert hashlib.sha256(raw).hexdigest()==s['decision_hash']


def test_withdraw_cannot_take_another_accounts_credit(env):
    submit(env)
    vm,c,bid,sponsor,researcher,attacker=env
    c.adjudicate_next(bid)
    vm.sender=attacker
    with pytest.raises(Exception,match='no credit'):c.withdraw()
    vm.sender=researcher;vm.origin=attacker
    with pytest.raises(Exception,match='directly'):c.withdraw()
    assert c.get_credit(str(researcher))==107


def test_no_adjudication_after_escape_boundary(env):
    submit(env)
    vm,c,bid,*_=env
    vm.warp('2026-10-08T00:10:01Z')
    with pytest.raises(Exception,match='closed'):c.adjudicate_next(bid)


def test_failed_first_then_qualifying_second(env):
    submit(env)
    vm,c,bid,sponsor,researcher,other=env
    second=REPORT+b'\nSecond attempt.\n'
    vm.sender=sponsor
    items=json.dumps([fp('second.md',second)])
    c.authorize_package(bid,str(other),items)
    vm.mock_web(re.escape(BASE+'second.md'),{'status':200,'body':second.decode()})
    vm.sender=other;vm.value=7;c.submit(bid,items);vm.value=0
    vm._llm_mocks=[]
    vm.mock_llm('You are a scientific methodology reviewer',json.dumps(result('INVALID_REPLICATION')))
    assert c.adjudicate_next(bid)=='INVALID_REPLICATION'
    vm._llm_mocks=[]
    r=result();r['citations']=[BASE+'second.md']
    vm.mock_llm('You are a scientific methodology reviewer',json.dumps(r))
    assert c.adjudicate_next(bid)=='FAILED_TO_REPLICATE'
    assert state(env)['winner']==1
    assert c.get_credit(str(other))==107
    assert c.get_credit(str(researcher))==7
    invariant(c)
