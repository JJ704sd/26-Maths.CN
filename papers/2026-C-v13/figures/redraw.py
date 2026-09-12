"""Rebuild paper vector figures from supplied records, without rerunning optimization."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1]
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','SimHei','DejaVu Sans'],'font.size':9,'axes.titlesize':10,'axes.labelsize':9,'xtick.labelsize':8,'ytick.labelsize':8,'legend.fontsize':8,'axes.spines.top':False,'axes.spines.right':False,'axes.unicode_minus':False,'pdf.fonttype':42})
BLUE='#24658B';ORANGE='#C56339';GRAY='#555D65';GOLD='#9B761D'
DATES=['2025-03-20','2025-06-21','2025-09-23','2025-12-21']
def read(q):return pd.read_csv(next((R/'完整代码').rglob(q+'_timeseries.csv'+('' if q=='q1' else '.gz'))))
def format_axis(ax):
 ax.set_xlim(0,24);ax.set_xticks(range(0,25,4));ax.grid(axis='y',alpha=.17);ax.set_xlabel('时刻 / h')
def step(ax,v,**kw):ax.step(np.arange(145)/6,np.r_[np.asarray(v),np.asarray(v)[-1]],where='post',**kw)
def save(fig,name):
 fig.savefig(R/'figures'/f'{name}.pdf',facecolor='white');plt.close(fig)
f=read('q1');fig,axes=plt.subplots(3,1,figsize=(6.3,4.0),sharex=True,layout='constrained')
step(axes[0],f.g,label='购电功率',color=BLUE);axes[0].plot(f.slot/6,f.load-f.pv,label='净负载',color=GRAY,lw=1);axes[0].set_ylabel('功率 / kW');axes[0].legend(ncol=2,loc='upper right')
axes[1].bar(f.slot/6,f.c,width=1/6,align='edge',color=BLUE,label='充电');axes[1].bar(f.slot/6,-f.d,width=1/6,align='edge',color=ORANGE,label='放电（负值）');axes[1].set_ylabel('功率 / kW');axes[1].legend(ncol=2,loc='upper right')
axes[2].plot(np.arange(145)/6,np.r_[f.soc_start.iloc[0],f.soc_end],color=BLUE);axes[2].axhline(1200,color=GRAY,ls=':',lw=.8);axes[2].axhline(10800,color=GRAY,ls=':',lw=.8);axes[2].set_ylabel('储电量 / kWh');axes[2].set_ylim(0,12000)
for ax in axes:format_axis(ax)
for ax in axes[:-1]:ax.set_xlabel('')
save(fig,'q1')
f=read('q2');fig,axes=plt.subplots(2,2,figsize=(6.3,5.7),layout='constrained')
for ax,date in zip(axes.flat,DATES):
 d=f[f.date==date];ax.set_title(date);ax.plot(d.slot/6,d.load-d.pv,color=GRAY,lw=1,label='实际净负载');ax.plot(d.slot/6,d.pred_load-d.pred_pv_0,color=GOLD,ls='--',lw=1,label='预测净负载');step(ax,d.original,color=BLUE,lw=1.1,label='合同购电');format_axis(ax);ax.set_ylabel('功率 / kW');ax.margins(y=.2);pass
fig.legend(*axes.flat[0].get_legend_handles_labels(),loc='outside upper center',ncol=3,frameon=False)
save(fig,'q2')
f=read('q3');fig=plt.figure(figsize=(6.3,6.1),layout='constrained');gs=fig.add_gridspec(4,2,height_ratios=[2,1,2,1])
for k,date in enumerate(DATES):
 row=2*(k//2);col=k%2;ax=fig.add_subplot(gs[row,col]);delta=fig.add_subplot(gs[row+1,col],sharex=ax);d=f[f.date==date]
 ax.set_title(date);step(ax,d.original,color=GRAY,ls='--',lw=1,label='零时合同');step(ax,d.final,color=BLUE,lw=1,label='最终合同');ax.set_ylabel('合同 / kW');ax.margins(y=.22)
 change=(d.final-d.original).to_numpy();delta.bar(d.slot/6,np.maximum(change,0),width=1/6,align='edge',color=BLUE);delta.bar(d.slot/6,np.minimum(change,0),width=1/6,align='edge',color=ORANGE);delta.axhline(0,color=GRAY,lw=.6);delta.set_ylabel('调整 / kW')
 for a in [ax,delta]:
  format_axis(a)
  for hour in [6,12,18]:a.axvline(hour,color=GOLD,ls=':',lw=.65)
 ax.set_xlabel('');ax.tick_params(labelbottom=False)
fig.legend(*fig.axes[0].get_legend_handles_labels(),loc='outside upper center',ncol=2,frameon=False)
save(fig,'q3')
f=read('q4_3');fig,axes=plt.subplots(2,2,figsize=(6.3,5.2),layout='constrained')
for ax,date in zip(axes.flat,DATES):
 d=f[f.date==date];ax.set_title(date);ax.plot(d.slot/6,d.price,color=GRAY,label='实际电价',lw=1);ax.plot(d.slot/6,d.pred_price,color=BLUE,ls='--',label='零时预测',lw=1.1);format_axis(ax);ax.set_ylim(bottom=0);ax.set_ylabel('电价 /（元/kWh）');pass
fig.legend(*axes.flat[0].get_legend_handles_labels(),loc='outside upper center',ncol=2,frameon=False)
save(fig,'q4price')
print('Four vector figures rebuilt')
