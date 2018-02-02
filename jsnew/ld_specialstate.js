module.exports = {
1:{id:1, name:"消耗次数", des:"该类状态会被行动消耗，每次行动消耗1层", function1:"", function2:"", function3:""}, 
21:{id:21, name:"眩晕", des:"下次出手不成功", function1:"", function2:"", function3:""}, 
23:{id:23, name:"忘却", des:"只能进行【普通攻击】", function1:"", function2:"", function3:""}, 
50:{id:50, name:"护卫", des:"免疫1次伤害", function1:"", function2:"", function3:""}, 
61:{id:61, name:"单技能增伤", des:"行动1次后会被消耗", function1:"", function2:"", function3:""}, 
93:{id:93, name:"火焰元素", des:"无属性变为火属性", function1:"", function2:"", function3:""}, 
100:{id:100, name:"心眼", des:"三回合内技能无消耗", function1:"3", function2:"", function3:""}, 
403:{id:403, name:"超凡入圣", des:"每消耗1点能量，回复[5*lv+50]点血量", function1:"5*lv+50", function2:"", function3:""}, 
1107:{id:1107, name:"恶魔真实", des:"攻击时附加$o[0.3*lv+0.8]%敌方最大生命值$w的真实伤害", function1:"(0.2*lv+1)/100*b.hp", function2:"", function3:""}, 
2302:{id:2302, name:"酒桶", des:"", function1:"200+20*lv+(100+8*lv)/100*a.ap", function2:"15", function3:"30"}, 
5706:{id:5706, name:"隐身", des:"", function1:"5704", function2:"5705", function3:""}, 
20152:{id:20152, name:"小英勇意志", des:"提高法术穿透数值相当于[0.5+0.3*lv]%的攻击力，提高护甲穿透数值相当于[0.5+0.3*lv]%的法术强度。", function1:"(0.5+0.3*lv)/100", function2:"", function3:""}, 
20156:{id:20156, name:"圣银弩箭", des:"必定为真实伤害", function1:"(0.1*lv+0.1)/100*b.hp", function2:"", function3:""}, 
30008:{id:30008, name:"", des:"行动时5%几率伤害变为火属性，持续1回合", function1:"5", function2:"", function3:""}, 
30009:{id:30009, name:"", des:"行动时5%几率伤害变为冰属性，持续1回合", function1:"5", function2:"", function3:""}, 
30047:{id:30047, name:"", des:"行动时5%几率伤害变为光属性，持续1回合", function1:"5", function2:"", function3:""}, 
30049:{id:30049, name:"", des:"自身【横扫千军】释放后，若敌方血量大于92%，80%几率再次释放【横扫千军】", function1:"5501", function2:"92", function3:"80"}, 
30050:{id:30050, name:"", des:"自身【狩物佛钉】释放后恢复60点能量", function1:"3201", function2:"60", function3:""}, 
30054:{id:30054, name:"", des:"行动时5%几率伤害变为暗属性，持续1回合", function1:"5", function2:"", function3:""}, 
30075:{id:30075, name:"通话3分钟", des:"初始能量增加至40，提高20点能量上限，每回合回复能量减少15点", function1:"40", function2:"15", function3:""}, 
30076:{id:30076, name:"通话5分钟", des:"初始能量增加至100，提高20点能量上限，每回合回复能量减少10点", function1:"100", function2:"10", function3:""}, 
30015:{id:30015, name:"物魔转换", des:"", function1:"", function2:"", function3:""}, 
31029:{id:31029, name:"杀意决1", des:"行动时10%几率使伤害变为暗属性，持续3回合", function1:"10", function2:"", function3:""}, 
32011:{id:32011, name:"", des:"只能【普通攻击】", function1:"", function2:"", function3:""}, 
40119:{id:40119, name:"割碎伤口", des:"割碎伤口：每1层流血，使伤害和持续伤害提高[0.4+0.08*lv]%", function1:"2", function2:"", function3:""}, 
40120:{id:40120, name:"灭杀", des:"暴击时可以灭杀（伤害提高20倍）血量少于[4+0.3*lv]%的对手（PVE效果降低为1/2）", function1:"(4+0.3*lv)/100", function2:"0.5", function3:"20"}, 
40314:{id:40314, name:"秘法连击", des:"每一次触发多重施法恢复[2+0.5*lv]点法力值", function1:"2+0.5*lv", function2:"", function3:""}, 
40516:{id:40516, name:"伤害和治疗", des:"行动1次后会被消耗", function1:"", function2:"", function3:""}, 
40519:{id:40519, name:"下一次连锁技能", des:"行动1次后会被消耗", function1:"", function2:"", function3:""}, 
40915:{id:40915, name:"连锁", des:"每回合连锁+1", function1:"1", function2:"", function3:""}, 
40916:{id:40916, name:"冰冻血莓", des:"【吟唱】，下3个冰霜技能伤害提高[3+1.35*lv]%", function1:"3+1.35*lv", function2:"", function3:""}, 
40917:{id:40917, name:"炽热烤肠", des:"【吟唱】，下3个火焰技能附加[3+1.5*lv]%伤害", function1:"3+1.5*lv", function2:"", function3:""}, 
40918:{id:40918, name:"光明雪梨", des:"【吟唱】，下3个光系技能获得[3+1.35*lv]%吸血", function1:"3+1.35*lv", function2:"", function3:""}, 
41044:{id:41044, name:"", des:"怒气，能量，法力回复速度提高10%", function1:"10", function2:"", function3:""}, 
30038:{id:30038, name:"天命", des:"行动时附加1~3999点随机伤害", function1:"math.random(1,3999)", function2:"", function3:""}, 
30030:{id:30030, name:"随缘巧篆", des:"变为随机属性", function1:"1910", function2:"", function3:""}}