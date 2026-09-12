from pathlib import Path
import numpy as np,pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
R=Path(__file__).resolve().parents[1]
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','SimHei','DejaVu Sans'],'font.size':9,'axes.labelsize':9,'xtick.labelsize':8,'ytick.labelsize':8,'legend.fontsize':8,'axes.spines.top':False,'axes.spines.right':False,'axes.unicode_minus':False,'pdf.fonttype':42})
fig,ax=plt.subplots(figsize=(6.3,1.9));fig.subplots_adjust(0,0,1,1);ax.set(xlim=(0,3),ylim=(0,1.9));ax.axis('off')
positions=[(.1,1.14),(1.1,1.14),(2.1,1.14),(2.1,.23),(1.1,.23),(.1,.23)]
labels=['历史与已发布信息\n限制决策时可用数据','预测与合同规划\n费用及储能约束','零时或更新合同\n仅调整尚未执行时段','实际观测与纠偏\n储能补足及紧急购电','实际库存与费用\n按真实价格结算','跨日反馈\n更新初值与历史样本']
for (x,y),label in zip(positions,labels):
 ax.add_patch(FancyBboxPatch((x,y),.8,.47,boxstyle='round,pad=.02',facecolor='#f0f4f7',edgecolor='#526978',lw=.8));ax.text(x+.4,y+.235,label,ha='center',va='center',fontsize=8)
for a,b in [((.92,1.375),(1.08,1.375)),((1.92,1.375),(2.08,1.375)),((2.5,1.10),(2.5,.74)),((2.08,.465),(1.92,.465)),((1.08,.465),(.92,.465)),((.5,.74),(.5,1.10))]:
 ax.annotate('',xy=b,xytext=a,arrowprops={'arrowstyle':'->','color':'#526978','lw':1})
fig.savefig(R/'figures/workflow.pdf');plt.close(fig)
fig,axs=plt.subplots(1,2,figsize=(6.3,2.3),layout='constrained')
for q,label,color,mark,style in [('q4_2','固定合同','#24658B','o','-'),('q4_3','滚动合同','#C56339','s','--')]:
 f=pd.read_csv(next((R/'完整代码').rglob(q+'_timeseries.csv.gz')));g=f.groupby(pd.to_datetime(f.date).dt.month)
 axs[0].plot(g.total_cost.sum()/1e4,label=label,color=color,marker=mark,ls=style,ms=3,lw=1)
 axs[1].plot(g.x.sum()/6000,label=label,color=color,marker=mark,ls=style,ms=3,lw=1)
for ax,title,y in zip(axs,['(a) 月度实际总费用','(b) 月度紧急购电量'],['费用 / 万元','紧急电量 / MWh']):
 ax.set(title=title,xlabel='月份',ylabel=y,xticks=range(2,13));ax.legend(frameon=False)
fig.savefig(R/'figures/monthly.pdf');plt.close(fig)
print('Workflow and monthly figures rebuilt from declared inputs.')
