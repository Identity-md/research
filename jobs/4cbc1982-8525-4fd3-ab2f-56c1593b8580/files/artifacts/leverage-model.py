#!/usr/bin/env python3
"""Offline analytical scenarios; NOT an exact v4 quote or fork simulation.
USD is an illustrative accounting unit; debts actually denominated in ETH/CLAUS.
C is net position collateral, N=L*C. Upfront charge and gas paid separately.
"""
import argparse
import json
import math
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR
F = 0.023
ETH_USD = 2700.0  # conversion assumption, not a market observation
P0 = 0.001       # hypothetical USD/CLAUS; not observed
IMPACT = 0.01    # per-leg adverse execution factor, not a live quote
GAS = 4.05      # 500k gas * 3 gwei * illustrative $2700/ETH
KEEPER = 2.0    # separate incentive; liquidation gas charged in addition
SERVICE = 1.0

def position(side, c=100.0, leverage=2.0, ratio=1.0, charge=0.01,
             impact=IMPACT, gas=GAS, keeper=0.0):
    if side not in ('long', 'short') or c <= 0 or leverage < 1 or ratio < 0 or not 0 <= impact < 1:
        raise ValueError('invalid scenario')
    n = c * leverage
    a = n * charge
    if side == 'long':
        debt = n-c  # ETH debt in illustrative USD at fixed ETH/USD
        q = n*(1-F)/(P0*(1+impact))
        gross_sale = q*P0*ratio/(1+impact)
        available = gross_sale*(1-F)
        paid = min(debt, max(0, available-gas-keeper))
        loss = debt-paid
        equity = max(0, available-gas-keeper-debt)
        fees = F*(n+gross_sale)
        debt_units = debt/ETH_USD
        repaid_units = paid/ETH_USD
        loss_current = loss
        be = (c+debt+2*gas+a)*(1+impact)**2/(n*(1-F)**2)
        impact_cost = n*ratio*(1-F)**2-available
        health = available/debt if debt else float('inf')
    else:
        debt = n  # short borrows N/P0 CLAUS, not (L-1)C
        q = n/P0
        proceeds = n*(1-F)/(1+impact)
        available = c+proceeds
        buy_cost = n*ratio*(1+impact)/(1-F)
        usable = max(0, available-gas-keeper)
        fraction = min(1, usable/buy_cost) if buy_cost else 1.0
        paid = n*fraction
        loss = n-paid  # loss valued at entry price; token loss persists
        equity = max(0, usable-buy_cost)
        fees = F*(n/(1+impact)+buy_cost)
        debt_units = q
        repaid_units = q*fraction
        loss_current = loss*ratio
        be = (proceeds-2*gas-a)*(1-F)/(n*(1+impact))
        impact_cost = n*(1-F)-proceeds + buy_cost-n*ratio/(1-F)
        health = available/buy_cost if buy_cost else float('inf')
    return dict(side=side,collateral=c,leverage=leverage,price_ratio=ratio,
                notional=n,debt_entry_value=debt,debt_units=debt_units,
                repaid_units=repaid_units,bad_debt_units=debt_units-repaid_units,
                provider_principal_loss_entry_value=loss,
                provider_principal_loss_current_value=loss_current,
                user_equity_after_exit=equity,user_net_pnl=equity-c-a-gas,
                gross_user_cash_before_open_gas=c+a+gas+KEEPER,
                opening_charge=a,pool_project_platform_fees=fees,project_fee=fees*20/23,platform_fee=fees*3/23,
                adverse_impact_cost=impact_cost,open_gas=gas,close_gas=gas,keeper_reward=keeper,
                exit_health=health,break_even_price_ratio=be,
                provider_net_after_service=a-loss-SERVICE)

def capital(c,l,k,longs):
    shorts=k-longs
    eth_loans=longs*(l-1)*c
    token_loans=shorts*l*c/P0
    # 80% utilization: segregated cash buffer, not posted collateral.
    return dict(collateral_per_user=c,leverage=l,positions=k,longs=longs,shorts=shorts,
      posted_collateral=k*c,eth_loans_usd=eth_loans,eth_inventory=eth_loans/.8/ETH_USD,
      claus_loans=token_loans,claus_inventory=token_loans/.8,
      unlent_buffer_usd=(eth_loans+token_loans*P0)*.25,
      long_locked_claus=longs*l*c*(1-F)/(P0*(1+IMPACT)),
      short_locked_proceeds_usd=shorts*l*c*(1-F)/(1+IMPACT),
      separate_first_loss_reserve_usd=.1*(eth_loans+token_loans*P0),
      separate_gas_reserve_usd=k*(2*GAS+KEEPER),
      actual_pool_depth=None)

def results():
    capital_rows=[capital(c,l,k,j) for c in [50,100,250,500] for l in [1.5,2]
      for k in [1,5,10] for j in sorted(set([0,k,k//2]))]
    costs=[position(s,c,l,charge=a) for c in [50,100,250,500]
       for l in [1.5,2] for s in ['long','short'] for a in [0,.005,.01,.015]]
    stress=[position(s,100,l,r,keeper=KEEPER) for s in ['long','short']
      for l in [1.5,2] for r in [.9,1.1,.75,1.25,.5,1.5,.1,3,11]]
    outages=[]
    for minutes in [1,5,30]:
      # Assumed stress trajectory: +/-1% compounded each minute. Not a probability estimate.
      for s,base in [('long',.99),('short',1.01)]:
        outages.append(dict(minutes=minutes,assumed_price_ratio=base**minutes,
                            result=position(s,100,2,base**minutes,keeper=KEEPER)))
    depth=100000.0  # hypothetical virtual USD quote reserve
    impact_budget=.005
    gross_cap=depth*impact_budget/(1-F)
    manipulation=[]
    for r in [1.1,1.25,2,3,11]:
      gross_push=depth*(math.sqrt(r)-1)/(1-F)
      # Fee-only irrecoverable lower bound, includes reversal sell. Excludes arbitrage/MEV.
      reverse_gross=depth*(math.sqrt(r)-1)
      fee_floor=F*(gross_push+reverse_gross)
      manipulation.append(dict(price_ratio=r,hypothetical_gross_push=gross_push,
                               fee_only_attack_cost_lower_bound=fee_floor))
    return dict(assumptions=dict(eth_usd=ETH_USD,claus_usd=P0,total_pool_fee=F,
      adverse_impact_per_leg=IMPACT,gas_per_transaction_usd=GAS,gas_units=500000,
      gas_gwei=3,keeper_reward_usd=KEEPER,service_usd_per_position=SERVICE,
      max_utilization=.8,first_loss_reserve_fraction_of_loans=.1),
      capital=capital_rows,costs=costs,stress=stress,keeper_outages=outages,
      capacity=dict(actual_executable_depth=None,authorized_live_positions=0,
        hypothetical_virtual_quote_reserve_usd=depth,average_impact_budget=impact_budget,
        hypothetical_gross_order_cap= gross_cap,
        collateral_cap_at_1_5x=gross_cap/1.5,collateral_cap_at_2x=gross_cap/2,
        aggregate_gross_close_cap=gross_cap,
        manipulation_examples=manipulation))

def self_test():
    for side in ['long','short']:
      for c in [50,100,250,500]:
       for l in [1.5,2]:
        for r in [.0,.1,.5,1,3,11]:
         x=position(side,c,l,r)
         assert x['pool_project_platform_fees'] >= 0
         assert abs(x['project_fee']+x['platform_fee']-x['pool_project_platform_fees'])<1e-8
         assert abs(x['debt_units']-x['repaid_units']-x['bad_debt_units'])<1e-7
         assert x['bad_debt_units']>=-1e-8 and x['user_equity_after_exit']>=0
         assert x['provider_principal_loss_entry_value']<=x['debt_entry_value']+1e-8
        be=position(side,c,l)['break_even_price_ratio']
        assert abs(position(side,c,l,be)['user_net_pnl'])<1e-8
    # explicit cash conservation on solvent and insolvent closes
    for r in [.1,1,11]:
      x=position('long',100,2,r,gas=0)
      available=200*(1-F)**2*r/(1+IMPACT)**2
      assert abs(available-x['repaid_units']*ETH_USD-x['user_equity_after_exit'])<1e-8
      x=position('short',100,2,r,gas=0)
      cash=100+200*(1-F)/(1+IMPACT)
      spent=x['repaid_units']*P0*r*(1+IMPACT)/(1-F)
      assert abs(cash-spent-x['user_equity_after_exit'])<1e-8
    assert position('long',ratio=.1)['bad_debt_units']>0
    assert position('short',ratio=11)['bad_debt_units']>0
    for n in [Decimal('0.0000000000000000011'),Decimal('1.2345678901234567899')]:
      scale=Decimal(10)**18
      debt=(n*scale).to_integral_value(rounding=ROUND_CEILING)
      payout=(n*scale).to_integral_value(rounding=ROUND_FLOOR)
      assert payout<=n*scale<=debt and debt-payout<=1
    assert capital(100,2,10,5)['eth_loans_usd']==500
    assert capital(100,2,10,5)['claus_loans']==1000000
    print('PASS: analytical conservation, asset debt repayment, fees, insolvency, break-even and directed rounding')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--self-test',action='store_true')
    args=p.parse_args()
    if args.self_test:self_test()
    else:print(json.dumps(results(),indent=2,allow_nan=False))
