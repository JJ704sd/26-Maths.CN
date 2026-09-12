"""Nine additional figures from supplied data; no optimization is rerun."""
from pathlib import Path
import json,hashlib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
R=Path(__file__).resolve().parents[1]
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','SimHei','DejaVu Sans'],'font.size':9,'axes.titlesize':10,'axes.labelsize':9,'xtick.labelsize':8,'ytick.labelsize':8,'legend.fontsize':8,'axes.spines.top':False,'axes.spines.right':False,'axes.unicode_minus':False,'pdf.fonttype':42})
B='#24658B';O='#C56339';G='#555D65';Y='#9B761D'
ledger={}
def load(name):
 p=next((R/'完整代码').rglob(name));ledger[str(p.relative_to(R))]=hashlib.sha256(p.read_bytes()).hexdigest();return pd.read_csv(p)
def save(fig,name):
 fig.savefig(R/'figures'/f'{name}.pdf',facecolor='white');plt.close(fig)
q1=load('q1_timeseries.csv');qs=[load(q+'_timeseries.csv.gz') for q in ['q2','q3','q4_2','q4_3']]
labels=['固定电价\n固定合同','固定电价\n滚动合同','波动电价\n固定合同','波动电价\n滚动合同']
# Same source and day/time layout as the heatmap supplied in the reference package.
p=R/'完整代码/问题4/输入数据/附件2.xlsx';ledger[str(p.relative_to(R))]=hashlib.sha256(p.read_bytes()).hexdigest()
raw=[pd.read_excel(p,sheet_name=k).iloc[:,1:].to_numpy(float) for k in [0,1]]
assert all(a.shape==(365,144) for a in raw)
fig,axs=plt.subplots(1,2,figsize=(6.3,2.6),layout='constrained')
starts=np.array([0,59,120,181,243,304,364]);monthlabs=['1月','3月','5月','7月','9月','11月','12月末']
for ax,a,title in zip(axs,raw,['(a) 实际负载','(b) 实际光伏']):
 im=ax.imshow(a,aspect='auto',origin='upper',extent=[0,24,365,0],cmap='cividis',rasterized=True)
 ax.set(title=title,xlabel='时刻 / h',ylabel='日期',xticks=[0,6,12,18,24],yticks=starts,yticklabels=monthlabs)
 cb=fig.colorbar(im,ax=ax,pad=.025);cb.set_label('功率 / kW')
save(fig,'annual_heatmap')
fig,axs=plt.subplots(1,2,figsize=(6.3,1.95),layout='constrained')
axs[0].plot(q1.slot/6,q1.load,label='负载',color=B);axs[0].plot(q1.slot/6,q1.pv,label='预测光伏',color=O,ls='--');axs[0].set_ylabel('功率 / kW');axs[0].legend(frameon=False,ncol=2)
axs[1].step(q1.slot/6,q1.price,where='post',color=B);axs[1].set_ylabel('电价 /（元/kWh）')
for ax,title in zip(axs,['(a) 代表日供需输入','(b) 已知分时电价']):ax.set(title=title,xlabel='时刻 / h',xlim=(0,24),xticks=[0,6,12,18,24])
save(fig,'day_inputs')
fig,ax=plt.subplots(figsize=(6.3,2.05),layout='constrained')
bp=ax.boxplot([f.soc_end.to_numpy()/1000 for f in qs],tick_labels=labels,showfliers=False,patch_artist=True,medianprops={'color':'black'})
for patch,color in zip(bp['boxes'],[B,O,B,O]):patch.set_facecolor(color);patch.set_alpha(.6)
for val in [1.2,10.8]:ax.axhline(val,ls='--',color=G,lw=.8)
ax.set_ylabel('时段末储电量 / MWh');ax.set_ylim(0,12)
save(fig,'soc_distribution')
errors=load('共同目标预报误差.csv.gz');sources=['前日18时原始','当日0时原始','当日6时原始','当日0时融合','当日6时融合']
fig,ax=plt.subplots(figsize=(6.3,2.1),layout='constrained')
ax.boxplot([errors.loc[errors.source==s,'error'].to_numpy() for s in sources],tick_labels=[s.replace('时','时\n') for s in sources],showfliers=False,whis=(5,95),patch_artist=True,boxprops={'facecolor':'#adc9d9'},medianprops={'color':'black'})
ax.axhline(0,color=G,lw=.8,ls='--');ax.set_ylabel('光伏预测误差 / kW')
save(fig,'forecast_error_distribution')
u=load('更新策略比较.csv');print('updates',u.to_dict('records'))
fig,axs=plt.subplots(1,2,figsize=(6.3,2.05),layout='constrained')
# Keep exact row order and labels from the supplied comparison records.
ulabs=['仅零时合同','每次重优化','价值触发']
axs[0].bar(ulabs,u.cost/1e4,color=[G,B,O]);axs[0].set_ylabel('实际费用 / 万元')
axs[1].bar(ulabs,u.emergency_kwh/1e4,color=[G,B,O]);axs[1].set_ylabel('紧急电量 / 万kWh')
for ax in axs:ax.tick_params(axis='x',labelsize=8)
save(fig,'update_comparison')
fig,ax=plt.subplots(figsize=(6.3,2.15),layout='constrained')
con=np.array([(f.total_cost-f.emergency_cost).sum()/1e4 for f in qs]);em=np.array([f.emergency_cost.sum()/1e4 for f in qs]);x=np.arange(4)
ax.bar(x,con,color=B,label='合同结算费');ax.bar(x,em,bottom=con,color=O,hatch='///',label='紧急购电费');ax.set_xticks(x,labels);ax.set_ylabel('费用 / 万元');ax.set_ylim(0,1850);fig.legend(*ax.get_legend_handles_labels(),ncol=2,frameon=False,loc='outside upper center')
for k in x:ax.text(k,con[k]+em[k]+15,f'{con[k]+em[k]:.2f}',ha='center',fontsize=8)
save(fig,'cost_components')
f=qs[3];delta=f.price-f.pred_price;mat=delta.to_numpy().reshape(334,144);v=float(np.abs(mat).max())
fig,ax=plt.subplots(figsize=(6.3,2.15),layout='constrained')
im=ax.imshow(mat,aspect='auto',origin='upper',extent=[0,24,334,0],cmap='cividis',vmin=-v,vmax=v,rasterized=True)
ax.set(xlabel='时刻 / h',ylabel='日期',xticks=[0,6,12,18,24],yticks=[0,89,181,273,333],yticklabels=['2月1日','5月1日','8月1日','11月1日','12月31日'])
fig.colorbar(im,ax=ax,pad=.02,label='实际价 − 零时预测价 /（元/kWh）')
save(fig,'price_error_heatmap')
s=load('安全分位数敏感性.csv');fig,axs=plt.subplots(1,2,figsize=(6.3,2.05),layout='constrained')
axs[0].plot(s.q,s.cost/1e4,'o-',color=B,label='实际费用');axs[0].plot(s.q,s.score/1e4,'s--',color=O,label='库存调整评分');axs[0].set_ylabel('费用或评分 / 万元');axs[0].legend(frameon=False,fontsize=7)
axs[1].plot(s.q,s.emergency_kwh,'o-',color=B);axs[1].set_ylabel('紧急电量 / kWh')
for ax in axs:ax.set_xlabel('安全分位数 q');ax.set_xticks([.6,.65,.7,.75,.8,.85,.9]);ax.tick_params(axis='x',labelsize=7)
save(fig,'risk_sensitivity')
s=load('单侧效率敏感性.csv');fig,axs=plt.subplots(1,2,figsize=(6.3,2.0),layout='constrained')
axs[0].plot(s.eta,s.cost/1e4,'o-',color=B);axs[0].set_ylabel('实际费用 / 万元')
axs[1].plot(s.eta,s.emergency_kwh/1e4,'s--',color=O);axs[1].set_ylabel('紧急电量 / 万kWh')
for ax in axs:ax.set_xlabel('单侧充放电效率');ax.set_xticks(s.eta)
save(fig,'efficiency_sensitivity')
stats={'price_zero_forecast_mae':float(delta.abs().mean()),'price_zero_forecast_rmse':float(np.sqrt((delta**2).mean())),'soc_median_kwh':[float(f.soc_end.median()) for f in qs],'source_sha256':ledger}
(R/'qa/new_figure_sources.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(stats,ensure_ascii=False,indent=2))
