# YGOPro Documentation Generator
Generate YGOPro Lua Documentation by automatically inspecting C++ source file

# Brief Description
This Python script generates `ygopro` Lua Documentation by automatically inspecting C++ source file. It's not really robust and it strongly relies on fixed coding convension (like spacing). This file can be used by `DataEditorX`, which havn't updated its `_functions.txt` for billions of year. Currently some coding convension fix (basically adding white space) need to be done to the upstream. Trying to create a Pull Requet.

# Usage
Simply put the script under `ygopro-core` master branch folder and run it. It outputs to STDOUT. Techincally it requires `python 3.x` and no other package (The regex module `re` is shipped as part of python). It probably can be easily modify it to `python 2.x` script by fixign the `print` statement. **It now also need old `_functions.txt` from DataEditorX**

# Example Output (Now much better)
    ●int Card.GetCode(card pcard)
     int[,int] Card.GetCode(Card c)
     返回c的当前代号（可能因为效果改变）
    ●int Card.GetOriginalCode(card pcard)
     int Card.GetOriginalCode(Card c)
     返回c的卡片记载的代号
    ●int Card.GetOriginalCodeRule(card pcard)
     int,int Card.GetOriginalCodeRule(Card c)
     返回c规则上的代号（这张卡规则上当作...使用）
    ●int Card.GetFusionCode(card pcard)
     int,int,... Card.GetFusionCode(Card c)
     返回c作为融合素材时的卡号（包括c原本的卡号）
    ●int Card.GetLinkCode(card pcard)
    ●bool Card.IsFusionCode(card pcard, nil|int tcode...)
     bool Card.IsFusionCode(Card c, int code)
     检查c作为融合素材时能否当作卡号为code的卡
    ●bool Card.IsLinkCode(card pcard, nil|int tcode...)
    ●bool Card.IsSetCard(card pcard, int set_code)
     bool Card.IsSetCard(Card c, int setname)
     检查c是否是卡名含有setname的卡
    ●bool Card.IsOriginalSetCard(card pcard, int set_code)
     bool Card.IsOriginalSetCard(Card c, int setname)
     检查c是否是原本卡名含有setname的卡
    ●bool Card.IsPreviousSetCard(card pcard, int set_code)
     bool Card.IsPreviousSetCard(Card c, int setname)
     检查c位置变化之前是否是名字含有setname的卡
    ●bool Card.IsFusionSetCard(card pcard, int set_code)
     bool Card.IsFusionSetCard(Card c, int setname)
     检查c作为融合素材时能否当作名字含有setname的卡
    ●bool Card.IsLinkSetCard(card pcard, int set_code)
    ●int Card.GetType(card pcard)
     int Card.GetType(Card c)
     返回c的当前类型
    ●int Card.GetOriginalType(card pcard)
     int Card.GetOriginalType(Card c)
     返回c的卡片记载的类型
    ●int Card.GetFusionType(card pcard)
     int Card.GetFusionType(Card c)
     返回c用作融合素材时的类型（与GetType的区别在于对于魔陷区的怪兽卡，返回其原本类型）
    ●int Card.GetSynchroType(card pcard)
    ●int Card.GetXyzType(card pcard)
    ●int Card.GetLinkType(card pcard)
    ●int Card.GetLevel(card pcard)
     int Card.GetLevel(Card c)
     返回c的当前等级
    ●int Card.GetRank(card pcard)
     int Card.GetRank(Card c)
     返回c的当前阶级
    ●int Card.GetLink(card pcard)
    ●int Card.GetSynchroLevel(card pcard, card scard)
     int Card.GetSynchroLevel(Card c, Card sc)
     返回c的对于同调怪兽sc的同调用等级
     此函数除了某些特定卡如调节支援士，返回值与Card.GetLevel(c)相同
    ●int Card.GetRitualLevel(card pcard, card scard)
     int Card.GetRitualLevel(Card c, Card rc)
     返回c的对于仪式怪兽rc仪式解放等级
     此函数除了某些特定卡如仪式供物，返回值与Card.GetLevel(c)相同
    ●int Card.GetOriginalLevel(card pcard)
     int Card.GetOriginalLevel(Card c)
     返回c的卡片记载的等级
    ●int Card.GetOriginalRank(card pcard)
     int Card.GetOriginalRank(Card c)
     返回c的卡片记载的阶级
    ●bool Card.IsXyzLevel(card pcard, card xyzcard, int lv)
     bool Card.IsXyzLevel(Card c, Card xyzc, int lv)
     检查c对于超量怪兽xyzc的超量用等级是否是lv
    ●int Card.GetLeftScale(card pcard)
     int Card.GetLeftScale(Card c)
     返回c的左灵摆刻度
    ●int Card.GetOriginalLeftScale(card pcard)
     int Card.GetOriginalLeftScale(Card c)
     返回c的原本的左灵摆刻度
    ●int Card.GetRightScale(card pcard)
     int Card.GetRightScale(Card c)
     返回c的右灵摆刻度
    ●int Card.GetOriginalRightScale(card pcard)
     int Card.GetOriginalRightScale(Card c)
     返回c的原本的右灵摆刻度
    ●bool Card.IsLinkMarker(card pcard, int dir)
    ●group Card.GetLinkedGroup(card pcard)
    ●int Card.GetLinkedGroupCount(card pcard)
    ●int Card.GetLinkedZone(card pcard, [nil|int cp])
    ●group Card.GetMutualLinkedGroup(card pcard)
    ●int Card.GetMutualLinkedGroupCount(card pcard)
    ●int Card.GetMutualLinkedZone(card pcard, [nil|int cp])
    ●bool Card.IsLinkState(card pcard)
    ●bool Card.IsExtraLinkState(card pcard)
    ●group Card.GetColumnGroup(card pcard)
    ●int Card.GetColumnGroupCount(card pcard)
    ●int Card.GetColumnZone(card pcard, int loc, [nil|int cp])
    ●bool Card.IsAllColumn(card pcard)
    ●int Card.GetAttribute(card pcard)
     int Card.GetAttribute(Card c)
     返回c的当前属性
     注：对某些多属性怪兽如光与暗之龙，此函数的返回值可能是几个属性的组合值
    ●int Card.GetOriginalAttribute(card pcard)
     int Card.GetOriginalAttribute(Card c)
     返回c的卡片记载的属性
    ●int Card.GetFusionAttribute(card pcard, [nil|int playerid])
     int Card.GetFusionAttribute(Card c[, int player])
     返回c[由player融合召唤时]用作融合素材时的属性
    ●int Card.GetLinkAttribute(card pcard, [nil|int playerid])
    ●int Card.GetRace(card pcard)
     int Card.GetRace(Card c)
     返回c的当前种族
     注：对某些多种族怪兽如动画效果的魔术猿，此函数的返回值可能是几个种族的组合值
    ●int Card.GetOriginalRace(card pcard)
     int Card.GetOriginalRace(Card c)
     返回c的卡片记载的种族
    ●int Card.GetLinkRace(card pcard, [nil|int playerid])
    ●int Card.GetAttack(card pcard)
     int Card.GetAttack(Card c)
     返回c的当前攻击力，返回值是负数表示是"?"
    ●int Card.GetBaseAttack(card pcard)
     int Card.GetBaseAttack(Card c)
     返回c的原本攻击力
    ●int Card.GetTextAttack(card pcard)
     int Card.GetTextAttack(Card c)
     返回c的卡片记载的攻击力
    ●int Card.GetBaseDefense(card pcard)
     int Card.GetBaseDefense(Card c)
     返回c的原本守备力
    ●int Card.GetTextDefense(card pcard)
     int Card.GetTextDefense(Card c)
     返回c的卡片记载的守备力
    ●int Card.GetPreviousCodeOnField(card pcard)
     int Card.GetPreviousCodeOnField(Card c)
     返回c位置变化之前的卡号
    ●int Card.GetPreviousTypeOnField(card pcard)
     int Card.GetPreviousTypeOnField(Card c)
     返回c位置变化之前的类型
    ●int Card.GetPreviousLevelOnField(card pcard)
     int Card.GetPreviousLevelOnField(Card c)
     返回c位置变化之前的等级
    ●int Card.GetPreviousRankOnField(card pcard)
     int Card.GetPreviousRankOnField(Card c)
     返回c位置变化之前的阶级
    ●int Card.GetPreviousAttributeOnField(card pcard)
     int Card.GetPreviousAttributeOnField(Card c)
     返回c位置变化之前的属性
    ●int Card.GetPreviousRaceOnField(card pcard)
     int Card.GetPreviousRaceOnField(Card c)
     返回c位置变化之前的种族
    ●int Card.GetPreviousAttackOnField(card pcard)
     int Card.GetPreviousAttackOnField(Card c)
     返回c位置变化之前的攻击力
    ●int Card.GetPreviousDefenseOnField(card pcard)
     int Card.GetPreviousDefenseOnField(Card c)
     返回c位置变化之前的守备力
    ●int Card.GetOwner(card pcard)
     int Card.GetOwner(Card c)
     返回c的持有者
    ●int Card.GetControler(card pcard)
     int Card.GetControler(Card c)
     返回c的当前控制者
    ●int Card.GetPreviousControler(card pcard)
     int Card.GetPreviousControler(Card c)
     返回c的位置变化之前的控制者
    ●int Card.GetReason(card pcard)
     int Card.GetReason(Card c)
     返回c的位置变化原因
    ●card Card.GetReasonCard(card pcard)
     Card Card.GetReasonCard(Card c)
     返回导致c的位置变化的卡
     此函数仅在某卡被战斗破坏时，因为上级召唤被解放，或者成为特殊召唤使用的素材时有效
    ●int Card.GetReasonPlayer(card pcard)
     int Card.GetReasonPlayer(Card c)
     返回导致c的位置变化的玩家
    ●effect Card.GetReasonEffect(card pcard)
     Effect Card.GetReasonEffect(Card c)
     返回导致c的位置变化的效果
    ●int Card.GetPosition(card pcard)
     int Card.GetPosition(Card c)
     返回c当前的表示形式
    ●int Card.GetPreviousPosition(card pcard)
     int Card.GetPreviousPosition(Card c)
     返回c位置变化前的表示形式
    ●int Card.GetBattlePosition(card pcard)
     int Card.GetBattlePosition(Card c)
     返回c在本次战斗发生之前的表示形式
    ●int Card.GetLocation(card pcard)
     int Card.GetLocation(Card c)
     返回c当前的所在位置
    ●int Card.GetPreviousLocation(card pcard)
     int Card.GetPreviousLocation(Card c)
     返回c位置变化前的所在的位置
    ●int Card.GetSequence(card pcard)
     int Card.GetSequence(Card c)
     返回c在当前位置的序号
     在场上时，序号代表所在的格子，从左往右分别是0-4，场地魔法格的序号为5，左右灵摆区域为6-7
     在其它地方时，序号表示的是第几张卡，最下面的卡的序号为0
    ●int Card.GetPreviousSequence(card pcard)
     int Card.GetPreviousSequence(Card c)
     返回c位置变化前的序号
    ●int Card.GetSummonType(card pcard)
     int Card.GetSummonType(Card c)
     返回c的召唤/特殊召唤的方式
    ●int Card.GetSummonLocation(card pcard)
     int Card.GetSummonLocation(Card c)
     返回c的召唤位置
    ●int Card.GetSummonPlayer(card pcard)
     int Card.GetSummonPlayer(Card c)
     返回召唤/特殊召唤c上场的玩家
    ●int Card.GetDestination(card pcard)
     int Card.GetDestination(Card c)
     返回c位置变化的目的地
     此函数仅在处理位置转移代替效果时有效
    ●int Card.GetLeaveFieldDest(card pcard)
     int Card.GetLeaveFieldDest(Card c)
     返回c离场时因改变去向的效果（如大宇宙）的目的地
    ●int Card.GetTurnID(card pcard)
     int Card.GetTurnID(Card c)
     返回c转移到当前位置的回合
    ●int Card.GetFieldID(card pcard)
     int Card.GetFieldID(Card c)
     返回c转移到当前位置的时间标识
     此数值唯一，越小表示c是越早出现在那个位置
     卡片从里侧翻开也会改变此数值
    ●int Card.GetRealFieldID(card pcard)
     int Card.GetRealFieldID(Card c)
     返回c转移到当前位置的真实的时间标识
     卡片从里侧翻开不会改变此数值
    ●bool Card.IsCode(card pcard, nil|int tcode...)
     bool Card.IsCode(Card c, int code1[, int code2,...])
     检查c的卡号是否是code1[, 或者为code2...]
    ●bool Card.IsType(card pcard, int ttype)
     bool Card.IsType(Card c, int type)
     检查c是否属于类型type
    ●bool Card.IsFusionType(card pcard, int ttype)
     bool Card.IsFusionType(Card c, int type)
     检查c用作融合素材时是否属于类型type（与IsType的区别在于对于魔陷区的怪兽卡，用其原本类型作判断）
    ●bool Card.IsSynchroType(card pcard, int ttype)
    ●bool Card.IsXyzType(card pcard, int ttype)
    ●bool Card.IsLinkType(card pcard, int ttype)
    ●bool Card.IsLevel(card pcard, nil|int tlevel...)
    ●bool Card.IsRank(card pcard, nil|int trank...)
    ●bool Card.IsLink(card pcard, nil|int tlink...)
    ●bool Card.IsAttack(card pcard, nil|int tatk...)
    ●bool Card.IsDefense(card pcard, nil|int tdef...)
    ●bool Card.IsRace(card pcard, int trace)
     bool Card.IsRace(Card c, int race)
     检查c是否属于种族race
    ●bool Card.IsLinkRace(card pcard, int trace, [nil|int playerid])
    ●bool Card.IsAttribute(card pcard, int tattrib)
     bool Card.IsAttribute(Card c, int attribute)
     检查c是否属于属性attribute
    ●bool Card.IsFusionAttribute(card pcard, int tattrib, [nil|int playerid])
     bool Card.IsFusionAttribute(Card c, int attribute[, int player])
     检查c[由player融合召唤时]用作融合素材是否属于属性attribute
    ●bool Card.IsLinkAttribute(card pcard, int tattrib, [nil|int playerid])
    ●bool Card.IsReason(card pcard, int treason)
     bool Card.IsReason(Card c, int reason)
     检查c是否包含原因reason
    ●bool Card.IsSummonType(card pcard, int ttype)
    ●bool Card.IsStatus(card pcard, int tstatus)
     bool Card.IsStatus(Card c, int status)
     检查c是否包含某个状态码
    ●bool Card.IsNotTuner(card pcard, card scard)
     bool Card.IsNotTuner(Card c)
     检查c是否可以当成非调整来使用
    ●nil Card.SetStatus(card pcard, int tstatus, bool enable)
     void Card.SetStatus(Card c, int state, bool enable)
     给c设置或者取消状态码
     除非妳清楚的了解每个状态码的含意，否则不要轻易使用此函数
    ●bool Card.IsDualState(card pcard)
     bool Card.IsDualState(Card c)
     检查c属否处于再召唤状态
    ●nil Card.EnableDualState(card pcard)
     void Card.EnableDualState(Card c)
     把c设置成再召唤状态
    ●int Card.GetTurnCounter(card pcard)
     int Card.GetTurnCounter(Card c)
     返回c的回合计数器
    ●nil Card.SetMaterial(card pcard, group|nil pgroup)
     void Card.SetMaterial(Card c, Group g)
     把g中的所有卡作为c的素材（上级召唤，特殊召唤）
    ●group Card.GetMaterial(card pcard)
     Group Card.GetMaterial(Card c)
     返回c出场使用的素材
    ●int Card.GetMaterialCount(card pcard)
     int Card.GetMaterialCount(Card c)
     返回c出场使用的素材数量
    ●group Card.GetEquipGroup(card pcard)
     Group Card.GetEquipGroup(Card c)
     返回c当前装备着的卡片组
    ●int Card.GetEquipCount(card pcard)
     int Card.GetEquipCount(Card c)
     返回c当前装备着的卡片数量
    ●card Card.GetEquipTarget(card pcard)
     Card Card.GetEquipTarget(Card c)
     返回c当前的装备对象
    ●card Card.GetPreviousEquipTarget(card pcard)
     Card Card.GetPreviousEquipTarget(Card c)
     返回c之前的装备对象
    ●bool Card.CheckEquipTarget(card pcard, [card target])
     bool Card.CheckEquipTarget(Card c1, Card c2)
     检查c2是否是c1的正确的装备对象
     ##由EFFECT_EQUIP_LIMIT效果或同盟状态确定
    ●int Card.GetUnionCount(card pcard)
     int Card.GetUnionCount(Card c)
     返回c当前装备的同盟卡数量
    ●group Card.GetOverlayGroup(card pcard)
     Group Card.GetOverlayGroup(Card c)
     返回c当前叠放着的卡片组
    ●int Card.GetOverlayCount(card pcard)
     int Card.GetOverlayCount(Card c)
     返回c当前叠放着的卡片数量
    ●card Card.GetOverlayTarget(card pcard)
     Card Card.GetOverlayTarget(Card c)
     返回以c为超量素材的卡
    ●bool Card.CheckRemoveOverlayCard(card pcard, int playerid, int count, int reason)
     bool Card.CheckRemoveOverlayCard(Card c, int player, int count, int reason)
     检查玩家player能否以reason为原因，至少移除c叠放的count张卡
    ●nil Card.RemoveOverlayCard(card pcard, int playerid, int min, int max, int reason)
     bool Card.RemoveOverlayCard(Card c, int player, int min, int max, int reason)
     以reason为原因，让玩家player移除c叠放的min-max张卡，返回值表示是否成功
    ●group Card.GetAttackedGroup(card pcard)
     Group Card.GetAttackedGroup(Card c)
     返回c本回合攻击过的卡片组
    ●int Card.GetAttackedGroupCount(card pcard)
     int Card.GetAttackedGroupCount(Card c)
     返回c本回合攻击过的卡片数量
    ●int Card.GetAttackedCount(card pcard)
     int Card.GetAttackedCount(Card c)
     返回c本回合攻击过的次数
     注：如果此值与上一个函数的返回值不同，那么说明此卡本回合进行过直接攻击
    ●group Card.GetBattledGroup(card pcard)
     Group Card.GetBattledGroup(Card c)
     返回与c本回合进行过战斗的卡片组
     进行过战斗指发生过伤害的计算，用于剑斗兽等卡的判定
    ●int Card.GetBattledGroupCount(card pcard)
     int Card.GetBattledGroupCount(Card c)
     返回与c本回合进行过战斗的的卡片数量
    ●int Card.GetAttackAnnouncedCount(card pcard)
     int Card.GetAttackAnnouncedCount(Card c)
     返回c本回合攻击宣言的次数
     注：攻击被无效不会被计入攻击过的次数，但是会计入攻击宣言的次数
    ●bool Card.IsDirectAttacked(card pcard)
     bool Card.IsDirectAttacked(Card c)
     检查c是否直接攻击过
    ●nil Card.SetCardTarget(card pcard, card ocard)
     void Card.SetCardTarget(Card c1, Card c2)
     把c2作为c1的永续对象
     c1和c2的联系会在c1或c2任意一卡离场或变成里侧表示时reset
    ●group Card.GetCardTarget(card pcard)
     Group Card.GetCardTarget(Card c)
     返回c当前所有的永续对象
    ●nil|card Card.GetFirstCardTarget(card pcard)
     Card Card.GetFirstCardTarget(Card c)
     返回c当前第一个永续对象
    ●int Card.GetCardTargetCount(card pcard)
     int Card.GetCardTargetCount(Card c)
     返回c当前的永续对象的数量
    ●bool Card.IsHasCardTarget(card pcard, card rcard)
     bool Card.IsHasCardTarget(Card c1, Card c2)
     检查c1是否取c2为永续对象
    ●nil Card.CancelCardTarget(card pcard, card rcard)
     void Card.CancelCardTarget(Card c1, Card c2)
     取消c2为c1的永续对象
    ●group Card.GetOwnerTarget(card pcard)
     Group Card.GetOwnerTarget(Card c)
     返回取c作为永续对象的所有卡
    ●int Card.GetOwnerTargetCount(card pcard)
     int Card.GetOwnerTargetCount(Card c)
     返回取c作为永续对象的卡的数量
    ●effect Card.GetActivateEffect(card pcard)
     Effect Card.GetActivateEffect(Card c)
     返回c的“卡片发动”的效果，即类型为EFFECT_TYPE_ACTIVATE的效果
     仅对魔法和陷阱有效
    ●group|effect|int Card.CheckActivateEffect(card pcard, bool neglect_con, bool neglect_cost, bool copy_info)
     Effect[,Group,int,int,Effect,int,int] Card.CheckActivateEffect(Card c, bool neglect_con, bool neglect_cost, bool copy_info)
     返回c的可以发动时机正确的“卡的发动”的效果，neglect_con=true则无视发动条件，neglect_cost=true则无视发动cost
     copy_info=false或者自由时点的效果则只返回这个效果
     否则还返回这个效果的时点为code的触发时点的信息 eg,ep,ev,re,r,rp
    ●function|nil|effect|int Card.GetTunerLimit(card pcard)
    ●function|nil|effect|int Card.GetHandSynchro(card pcard)
    ●int Card.RegisterEffect(card pcard, effect peffect, [bool forced])
     int Card.RegisterEffect(Card c, Effect e[, bool forced=false])
     把效果e注册给c，返回效果的全局id，并设置e的Handler为c
     默认情况下注册时如果c带有免疫e的效果那么注册会失败
     如果forced为true则不会检查c对e的免疫效果
    ●nil|effect Card.IsHasEffect(card pcard, int code)
     bool Card.IsHasEffect(Card c, int code)
     检查c是否受到效果种类是code的效果的影响
    ●nil Card.ResetEffect(card pcard, int code, int type)
     void Card.ResetEffect(Card c, int reset_code, int reset_type)
     以重置类型为reset_type、重置种类为reset_code手动重置c受到的效果的影响
     reset_type只能是以下类型，对应的重置种类为
     RESET_EVENT       发生事件重置        reset_code为事件
     RESET_PHASE       阶段结束重置        reset_code为阶段
     RESET_CODE        重置指定code的效果  reset_code为效果的种类code，只能重置EFFECT_TYPE_SINGLE的永续型效果
     RESET_COPY        重置复制的效果      reset_code为copy_id
     RESET_CARD        重置卡片的效果      reset_code为效果owner的卡号
    ●int Card.GetEffectCount(card pcard, int code)
     int Card.GetEffectCount(Card c, int code)
     返回c受到影响的种类是code的效果的数量
    ●effect Card.RegisterFlagEffect(card pcard, int code, int reset, int flag, int count, [int lab, int desc])
     Effect Card.RegisterFlagEffect(Card c, int code, int reset_flag, int property, int reset_count[, int label, int desc])
     为c注册一个标识用效果
     注：注册给卡的标识用效果不会用于系统，
     即使code与内置效果code重合也不会影响，
     并且类型总是EFFECT_TYPE_SINGLE，reset方法，property和一般的效果相同，
     并且不会无效化，不受卡的免疫效果影响
    ●int Card.GetFlagEffect(card pcard, int code)
     int Card.GetFlagEffect(Card c, int code)
     返回c的种类是code的标识效果的数量
    ●nil Card.ResetFlagEffect(card pcard, int code)
     void Card.ResetFlagEffect(Card c, int code)
     手动清除c的种类是code的标识效果
    ●bool Card.SetFlagEffectLabel(card pcard, int code, int lab)
     bool Card.SetFlagEffectLabel(Card c, int code, int label)
     返回c是否存在种类为code的标识效果，并设置其Label属性为label
    ●nil|int Card.GetFlagEffectLabel(card pcard, int code)
     int Card.GetFlagEffectLabel(Card c, int code)
     返回c的种类为code的标识效果的Label，没有此效果则返回nil
    ●nil Card.CreateRelation(card pcard, card rcard, int reset)
     void Card.CreateRelation(Card c1, Card c2, int reset_flag)
     为c1建立于c2的联系此联系，仅会由于c1发生RESET_EVENT的事件reset
    ●nil Card.ReleaseRelation(card pcard, card rcard)
     void Card.ReleaseRelation(Card c1, Card c2)
     手动释放c1对于c2的联系
    ●nil Card.CreateEffectRelation(card pcard, effect peffect)
     void Card.CreateEffectRelation(Card c, Effect e)
     为卡片c和效果e建立联系
    ●nil Card.ReleaseEffectRelation(card pcard, effect peffect)
     void Card.ReleaseEffectRelation(Card c,Effect e)
     手动释放c与效果e的联系
    ●nil Card.ClearEffectRelation(card pcard)
     void Card.ClearEffectRelation(Card c)
     清空c所有联系的效果
    ●bool Card.IsRelateToEffect(card pcard, effect peffect)
     bool Card.IsRelateToEffect(Card c, Effect e)
     检查c是否和效果e有联系
     注：每次发动进入连锁的效果时，发动效果的卡，以及发动效果时指定的对象
     （用Duel.SetTargetCard或者Duel.SelectTarget指定的，包括取对象和不取对象）
    ●bool Card.IsRelateToChain(card pcard, int chain_count)
     bool Card.IsRelateToChain(Card c, int chainc)
     检查c是否和连锁chainc有联系
     注：每次发动进入连锁的效果时，发动效果的卡，以及发动效果时指定的对象
     （用Duel.SetTargetCard或者Duel.SelectTarget指定的，包括取对象和不取对象）
     会自动与那个效果建立联系，一旦离场，联系会重置
    ●bool Card.IsRelateToCard(card pcard, card rcard)
     bool Card.IsRelateToCard(Card c1, Card c2)
     检查c1是否和c2有联系
    ●bool Card.IsRelateToBattle(card pcard)
     bool Card.IsRelateToBattle(Card c)
     检查c是否和本次战斗关联
     注：此效果通常用于伤害计算后伤害阶段结束前，用于检查战斗的卡是否离场过
    ●int Card.CopyEffect(card pcard, int code, int reset, [int count])
     int Card.CopyEffect(Card c, int code, int reset_flag[, int reset_count])
     为c添加卡号是code的卡的可复制的效果，并且添加额外的reset条件
     返回值是表示复制效果的代号id
    ●int Card.ReplaceEffect(card pcard, int code, int reset, [int count])
     int Card.ReplaceEffect(Card c, int code, int reset_flag[, int reset_count])
     把c的效果替换为卡号是code的卡的效果，并且添加额外的reset条件
     返回值是表示替换效果的代号id
    ●nil Card.EnableUnsummonable(card pcard)
     void Card.EnableUnsummonable(Card c)
     将c设置为不可通常召唤的怪兽
     ##实际上是个不可复制、不会被无效的EFFECT_UNSUMMONABLE_CARD效果
    ●nil Card.EnableReviveLimit(card pcard)
     void Card.EnableReviveLimit(Card c)
     为c添加苏生限制
     ##实际上是不可复制、不会被无效的EFFECT_UNSUMMONABLE_CARD和EFFECT_REVIVE_LIMIT效果
    ●nil Card.CompleteProcedure(card pcard)
     void Card.CompleteProcedure(Card c)
     使c完成正规的召唤手续
     ##此函数也可通过Card.SetStatus实现
    ●bool Card.IsDisabled(card pcard)
     bool Card.IsDisabled(Card c)
     检查c是否处于无效状态
    ●bool Card.IsDestructable(card pcard, [effect peffect])
     bool Card.IsDestructable(Card c[, Effect e])
     检查c是否是可破坏的
    ●bool Card.IsSummonableCard(card pcard)
     bool Card.IsSummonableCard(Card c)
     检查c是否是可通常召唤的卡
    ●bool Card.IsFusionSummonableCard(card pcard, [int summon_type])
     bool Card.IsFusionSummonableCard(Card c)
     检查c是否是可融合召唤的卡
    ●bool Card.IsSpecialSummonable(card pcard, [int sumtype])
     bool Card.IsSpecialSummonable(Card c)
     检查是否可以对c进行特殊召唤手续
    ●bool Card.IsSynchroSummonable(card pcard, nil|card tuner, [group|nil mg])
     bool Card.IsSynchroSummonable(Card c ,Card tuner|nil[, Group mg])
     检查是否可以以tuner作为调整，场上的卡[或mg]为同调素材对c进行同调召唤手续
     如果tuner是nil，此函数与Card.IsSpecialSummonable作用相同
    ●bool Card.IsXyzSummonable(card pcard, group|nil materials, [int minc, int maxc])
     bool Card.IsXyzSummonable(Card c, Group mg|nil[, min=0, max=0])
     检查是否可以在mg中选出[min-max个]超量素材对c进行超量召唤手续
     如果mg为nil，此函数与Card.IsSpecialSummonable作用相同
    ●bool Card.IsSummonable(card pcard, bool ign, nil|effect peffect, [int minc, int zone])
     bool Card.IsSummonable(Card c, bool ignore_count, Effect e|nil[, int min=0])
     检查c是否进行通常召唤（不包含通常召唤的set)，ignore_count=true则不检查召唤次数限制
     e~=nil则检查c是否可以以效果e进行通常召唤，min表示至少需要的祭品数（用于区分妥协召唤与上级召唤）
    ●bool Card.IsMSetable(card pcard, bool ign, nil|effect peffect, [int minc, int zone])
     bool Card.IsMSetable(Card, bool ignore_count, Effect e|nil[, int min=0])
     检查c是否可进行通常召唤的set，ignore_count=true则不检查召唤次数限制
     e~=nil则检查c是否可以以效果e进行通常召唤的set，min表示至少需要的祭品数（用于区分妥协召唤set与上级召唤set）
    ●bool Card.IsSSetable(card pcard, [bool ign])
     bool Card.IsSSetable(Card c[, bool ignore_field=false])
     检查c是否可以set到魔法陷阱区，ignore_field=true则无视魔陷区格子限制
    ●bool Card.IsCanBeSpecialSummoned(card pcard, effect peffect, int sumtype, int sumplayer, bool nocheck, bool nolimit, [int sumpos, int toplayer, int zone])
     bool Card.IsCanBeSpecialSummoned(Card c, Effect e, int sumtype, int sumplayer, bool nocheck, bool nolimit[, int sumpos=POS_FACEUP, int target_player=sumplayer])
     检查c是否可以被玩家sumplayer用效果e以sumtype方式和sumpos表示形式特殊召唤到target_player场上
     如果nocheck是true则不检查c的召唤条件，如果nolimit是true则不检查c的苏生限制
    ●bool Card.IsAbleToHand(card pcard)
     bool Card.IsAbleToHand(Card c)
     检查c是否可以送去手牌
     注：仅当卡片或者玩家受到“不能加入手牌”的效果的影响时（如雷王）此函数才返回false
     ##以下几个函数类似
    ●bool Card.IsAbleToDeck(card pcard)
     bool Card.IsAbleToDeck(Card c)
     检查c是否可以送去卡组
    ●bool Card.IsAbleToExtra(card pcard)
     bool Card.IsAbleToExtra(Card c)
     检查c是否可以送去额外卡组
     对于非融合，同调，超量卡此函数均返回false
    ●bool Card.IsAbleToGrave(card pcard)
     bool Card.IsAbleToGrave(Card c)
     检查c是否可以送去墓地
    ●bool Card.IsAbleToRemove(card pcard, [int p])
     bool Card.IsAbleToRemove(Card c[, int player])
     检查c是否可以被玩家player除外
    ●bool Card.IsAbleToHandAsCost(card pcard)
     bool Card.IsAbleToHandAsCost(Card c)
     检查c是否可以作为cost送去手牌
     注：此函数会在Card.IsAbleToHand的基础上追加检测c的实际目的地
     当c送往手牌会被送去其它地方时（如缩退回路适用中，或者c是融合，同调和超量怪的一种），此函数返回false
     ##以下几个函数类似
    ●bool Card.IsAbleToDeckAsCost(card pcard)
     bool Card.IsAbleToDeckAsCost(Card c)
     检查c是否可以作为cost送去卡组
    ●bool Card.IsAbleToExtraAsCost(card pcard)
     bool Card.IsAbleToExtraAsCost(Card c)
     检查c是否可以作为cost送去额外卡组
    ●bool Card.IsAbleToDeckOrExtraAsCost(card pcard)
     bool Card.IsAbleToDeckOrExtraAsCost(Card c)
     检查c是否可以作为cost送去卡组或额外卡组（用于新宇侠、剑斗兽融合怪兽的召唤手续检测）
    ●bool Card.IsAbleToGraveAsCost(card pcard)
     bool Card.IsAbleToGraveAsCost(Card c)
     检查c是否可以作为cost送去墓地
    ●bool Card.IsAbleToRemoveAsCost(card pcard)
     bool Card.IsAbleToRemoveAsCost(Card c)
     检查c是否可以作为cost除外
    ●bool Card.IsReleasable(card pcard)
     bool Card.IsReleasable(Card c)
     检查c是否可以被解放（非上级召唤用）
    ●bool Card.IsReleasableByEffect(card pcard)
     bool Card.IsReleasableByEffect(Card c)
     检查c是否可以被效果解放
    ●bool Card.IsDiscardable(card pcard, [int reason])
     bool Card.IsDiscardable(Card[, int reason=REASON_COST])
     检查c是否可以丢弃
     注：此函数仅用于检测，
     以REASON_DISCARD作为原因把一张手卡送墓并不会导致那张卡不能丢弃
    ●bool Card.IsAttackable(card pcard)
     bool Card.IsAttackable(Card c)
     检查c是否可以攻击
    ●bool Card.IsChainAttackable(card pcard, [int ac, bool monsteronly])
     bool Card.IsChainAttackable(Card c[, int ac = 2, bool monsteronly = false])
     检查c是否可以连续攻击，c的攻击宣言次数>=ac则返回false
     注：当c因为闪光之双剑等效果进行过多次攻击之后此函数返回false
    ●bool Card.IsFaceup(card pcard)
     bool Card.IsFaceup(Card c)
     检查c是否是表侧表示
    ●bool Card.IsAttackPos(card pcard)
     bool Card.IsAttackPos(Card c)
     检查c是否是攻击表示
    ●bool Card.IsFacedown(card pcard)
     bool Card.IsFacedown(Card c)
     检查c是否是里侧表示
    ●bool Card.IsDefensePos(card pcard)
     bool Card.IsDefensePos(Card c)
     检查c是否是守备表示
    ●bool Card.IsPosition(card pcard, int pos)
     bool Card.IsPosition(Card c, int pos)
     检查c是否是表示形式pos
    ●bool Card.IsPreviousPosition(card pcard, int pos)
     bool Card.IsPreviousPosition(Card c, int pos)
     检查c位置变化之前是否是表示形式pos
    ●bool Card.IsControler(card pcard, int con)
     bool Card.IsControler(Card c, int controler)
     检查c的当前控制着是否是controler
    ●bool Card.IsOnField(card pcard)
     bool Card.IsOnField(Card c)
     检查c是否在场
     注：当怪兽召唤，反转召唤，特殊召唤时召唤成功之前，此函数返回false
    ●bool Card.IsLocation(card pcard, int loc)
     bool Card.IsLocation(Card c, int location)
     检查c当前位置是否是location
     注：当怪兽召唤，反转召唤，特殊召唤时召唤成功之前，
     并且location=LOCATION_MZONE时，此函数返回false
    ●bool Card.IsPreviousLocation(card pcard, int loc)
     bool Card.IsPreviousLocation(Card c, int location)
     检查c之前的位置是否是location
    ●bool Card.IsLevelBelow(card pcard, int lvl)
     bool Card.IsLevelBelow(Card c, int level)
     检查c是否是等级level以下（至少为1）
    ●bool Card.IsLevelAbove(card pcard, int lvl)
     bool Card.IsLevelAbove(Card c, int level)
     检查c是否是等级level以上
    ●bool Card.IsRankBelow(card pcard, int rnk)
     bool Card.IsRankBelow(Card c, int rank)
     检查c是否是阶级rank以下（至少为1）
    ●bool Card.IsRankAbove(card pcard, int rnk)
     bool Card.IsRankAbove(Card c, int rank)
     检查c是否是阶级rank以上
    ●bool Card.IsLinkBelow(card pcard, int lnk)
    ●bool Card.IsLinkAbove(card pcard, int lnk)
    ●bool Card.IsAttackBelow(card pcard, int atk)
     bool Card.IsAttackBelow(Card c, int atk)
     检查c是否是攻击力atk以下（至少为0）
    ●bool Card.IsAttackAbove(card pcard, int atk)
     bool Card.IsAttackAbove(Card c, int atk)
     检查c是否是攻击力atk以上
    ●bool Card.IsDefenseBelow(card pcard, int def)
     bool Card.IsDefenseBelow(Card c, int def)
     检查c是否是守备力def以下（至少为0）
    ●bool Card.IsDefenseAbove(card pcard, int def)
     bool Card.IsDefenseAbove(Card c, int def)
     检查c是否是守备力def以上
    ●bool Card.IsPublic(card pcard)
     bool Card.IsPublic(Card c)
     检查c是否处于公开状态
    ●bool Card.IsForbidden(card pcard)
     bool Card.IsForbidden(Card c)
     检查c是否处于被宣言禁止状态
    ●bool Card.IsAbleToChangeControler(card pcard)
     bool Card.IsAbleToChangeControler(Card c)
     检查c是否可以改变控制权
     注：仅当卡收到了“不能改变控制权”的效果的影响时，此函数返回false
    ●bool Card.IsControlerCanBeChanged(card pcard, [bool ign, int zone])
     bool Card.IsControlerCanBeChanged(Card c)
     检查c的控制权是否可以改变
     注：此函数会在Card.IsAbleToChangeControler的基础上追加检测场上的空格位
    ●bool Card.AddCounter(card pcard, int countertype, int count, [bool singly])
     bool Card.AddCounter(Card c, int countertype, int count[, int singly=false])
     为c放置count个countertype类型的指示物，singly为true表示逐个添加至上限为止
    ●nil Card.RemoveCounter(card pcard, int rplayer, int countertype, int count, int reason)
     void Card.RemoveCounter(Card c, int player, int countertype, int count, int reason)
     让玩家player以原因reason移除c上的count个countertype类型的指示物
    ●int Card.GetCounter(card pcard, int countertype)
     int Card.GetCounter(Card c, int countertype)
     返回c上的countertype类型的指示物的数量
    ●nil Card.EnableCounterPermit(card pcard, int countertype, [int prange])
     void Card.EnableCounterPermit(Card c, int countertype[, int location])
     允许c[在位置location]放置那个需要“可以放置”才能放置的指示物countertype
     location的默认值与c的种类有关，灵摆怪兽需要指定能否在怪兽区域或灵摆区域放置指示物
    ●nil Card.SetCounterLimit(card pcard, int countertype, int limit)
     void Card.SetCounterLimit(Card c, int countertype, int count)
     设定c放置countertype类型指示物的上限
    ●bool Card.IsCanChangePosition(card pcard)
    ●bool Card.IsCanTurnSet(card pcard)
     bool Card.IsCanTurnSet(Card c)
     检查c是否可以转成里侧表示
    ●bool Card.IsCanAddCounter(card pcard, int countertype, int count, [bool singly, int loc])
     bool Card.IsCanAddCounter(Card c, int countertype, int count[, int singly=false])
     检查c是否可以[逐个(singly=true)]放置count个countertype类型的指示物
    ●bool Card.IsCanRemoveCounter(card pcard, int playerid, int countertype, int count, int reason)
     bool Card.IsCanRemoveCounter(Card c, int player, int countertype, int count, int reason)
     检查玩家player是否可以以原因reason移除c上的count个countertype类型的指示物
    ●bool Card.IsCanBeFusionMaterial(card pcard, [nil|card fcard])
     bool Card.IsCanBeFusionMaterial(Card c[, Card fc])
     检查c是否可以成为[融合怪兽fc的]融合素材
    ●bool Card.IsCanBeSynchroMaterial(card pcard, [card scard, card tuner])
     bool Card.IsCanBeSynchroMaterial(Card c[, Card sc, Card tuner])
     检查c是否可以成为同调怪兽sc的同调素材
    ●bool Card.IsCanBeRitualMaterial(card pcard, nil|card scard)
     bool Card.IsCanBeRitualMaterial(Card c[, Card sc])
     检查c是否能作为仪式怪兽sc的祭品
    ●bool Card.IsCanBeXyzMaterial(card pcard, nil|card scard)
     bool Card.IsCanBeXyzMaterial(Card c, Card sc|nil)
     检查c是否可以成为超量怪兽sc的超量素材
    ●bool Card.IsCanBeLinkMaterial(card pcard, nil|card scard)
    ●bool Card.CheckFusionMaterial(card pcard, [group|nil pgroup, nil|card cg, int chkf])
     bool Card.CheckFusionMaterial(Card c[, Group g, Card gc|nil, int chkf=PLAYER_NONE])
     检查g是否包含了c需要[必须包含gc在内]的一组融合素材
     ##根据c的种类为EFFECT_FUSION_MATERIAL的效果的Condition函数检查
    ●bool Card.CheckFusionSubstitute(card pcard, card fcard)
     bool Card.CheckFusionSubstitute(Card c, Card fc)
     检查c能否代替融合怪兽fc的记述卡名的素材
    ●bool Card.IsImmuneToEffect(card pcard, effect peffect)
     bool Card.IsImmuneToEffect(Card c, Effect e)
     检查c是否免疫效果e（即不受效果e的影响）
    ●bool Card.IsCanBeEffectTarget(card pcard, [effect peffect])
     bool Card.IsCanBeEffectTarget(Card c, Effect e)
     检查c是否可以成为效果e的对象
    ●bool Card.IsCanBeBattleTarget(card pcard, card bcard)
     bool Card.IsCanBeBattleTarget(Card c1, Card c2)
     检查c1是否可以成为c2的攻击目标
    ●nil Card.AddMonsterAttribute(card pcard, int type, [int attribute, int race, int level, int atk, int def])
     void Card.AddMonsterAttribute(Card c, int attribute, int race, int level, int atk, int def)
     为魔陷卡c添加怪兽数值
     注：在数据库中有记录的数值视为原本数值，此处设置为0
    ●nil Card.AddMonsterAttributeComplete()
    ●nil Card.CancelToGrave(card pcard, [bool cancel])
     void Card.CancelToGrave(Card c[, bool cancel=true])
     取消送墓确定状态，cancel=false则重新设置送墓确定状态
     注：送墓确定状态指的是在场上发动的不留场的魔法和陷阱后，这些卡片的状态
     送墓确定状态中的卡无法返回手牌和卡组，并且连锁结束时送去墓地
     此函数的作用是取消此状态使其留场，用于光之护封剑和废铁稻草人等卡
    ●int Card.GetTributeRequirement(card pcard)
     int,int Card.GetTributeRequirement(Card c)
     返回通常召唤c所需要的祭品的最小和最大数量
    ●nil|card Card.GetBattleTarget(card pcard)
     Card Card.GetBattleTarget(Card c)
     返回与c进行战斗的卡
    ●bool|group Card.GetAttackableTarget(card pcard)
     Group,bool Card.GetAttackableTarget(Card c)
     返回c可攻击的卡片组以及能否直接攻击
    ●nil Card.SetHint(card pcard, int type, int value)
     void Card.SetHint(Card c, int type, int value)
     为c设置类型为type的卡片提示信息
     type只能为以下值，对应的value类型为
     CHINT_TURN              回合数
     CHINT_CARD              卡片id
     CHINT_RACE              种族
     CHINT_ATTRIBUTE         属性
     CHINT_NUMBER            数字
     CHINT_DESC              描述
    ●nil Card.ReverseInDeck(card pcard)
     void Card.ReverseInDeck(Card c)
     设置c在卡组中正面表示
    ●nil Card.SetUniqueOnField(card pcard, int unique_pos[0], int unique_pos[1], function|int unique_function|unique_code, [int location])
     void Card.SetUniqueOnField(Card c, int s, int o, int unique_code[, int unique_location=LOCATIOIN_ONFIELD])
     设置c以unique_code只能在场上[或怪兽区域或魔陷区域，由unique_location决定]只能存在1张
     s不为0会检查自己场上的唯一性，o不为0则检查对方场上的唯一性
    ●bool Card.CheckUniqueOnField(card pcard, int check_player, [int check_location, card icard])
     bool Card.CheckUniqueOnField(Card c,int check_player)
     检查c在check_player场上的唯一性
    ●nil Card.ResetNegateEffect(card pcard, [int ?...])
     void Card.ResetNegateEffect(Card c[, int code1,...])
     重置c受到的卡号为code1, code2...的卡片的效果的影响
    ●nil Card.AssumeProperty(card pcard, int assume_type, int assume_value)
     void Card.AssumeProperty(Card c,int assume_type, int assume_value)
     把c的assume_type的数值当作assume_value使用（基因组斗士）
     assume_type为以下类型
     ASSUME_CODE         卡号
     ASSUME_TYPE         类型
     ASSUME_LEVEL        等级
     ASSUME_RANK         阶级
     ASSUME_ATTRIBUTE    属性
     ASSUME_RACE         种族
     ASSUME_ATTACK       攻击力
     ASSUME_DEFENSE      守备力
    ●nil Card.SetSPSummonOnce(card pcard, int spsummon_code)
     void Card.SetSPSummonOnce(Card c, int spsummon_code)
     设置c一回合只能进行1次特殊召唤（灵兽，波动龙）
     相同的spsummon_code共用1个次数
    ●effect Effect.CreateEffect(card pcard)
     Effect Effect.CreateEffect(Card c)
     新建一个空效果
     并且效果的Owner为c
    ●effect Effect.GlobalEffect()
     Effect Effect.GlobalEffect()
     新建一个全局效果
    ●effect Effect.Clone(effect peffect)
     Effect Effect.Clone(Effect e)
     新建一个效果e的副本
    ●nil Effect.Reset(effect peffect)
     void Effect.Reset(Effect e)
     把效果e重置，重置之后不可以再使用此效果
    ●int Effect.GetFieldID(effect peffect)
     int Effect.GetFieldID(Effect e)
     获取效果e的id
    ●nil Effect.SetDescription(effect peffect, int v)
     void Effect.SetDescription(Effect e, int desc)
     为效果e设置效果描述
    ●nil Effect.SetCode(effect peffect, int v)
     void Effect.SetCode(Effect e, int code)
     为效果e设置Code属性
    ●nil Effect.SetRange(effect peffect, int v)
     void Effect.SetRange(Effect e, int range)
     为效果e设置Range属性
    ●nil Effect.SetTargetRange(effect peffect, int s, int o)
     void Effect.SetTargetRange(Effect e, int s_range, int o_range)
     为效果e设置Target Range属性
        s_range指影响的我方区域
        o_range值影响的对方区域
        如果property属性中指定了EFFECT_FLAG_ABSOLUTE_RANGE标志，
            那么s_range指玩家1受到影响的区域，o_range指玩家2受到影响的区域
        如果这是一个召唤(覆盖)/限制召唤(覆盖)/特殊召唤手续
        (EFFECT_SUMMON_PROC/EFFECT_LIMIT_SUMMON_PROC/EFFECT_SPSUMMON_PROC等)的效果，
            并且property指定了EFFECT_FLAG_SPSUM_PARAM标志，
            那么s_range表示特殊召唤到的哪个玩家的场地，
        o_range表示可选择的表示形式
    ●nil Effect.SetAbsoluteRange(effect peffect, int playerid, int s, int o)
     void Effect.SetAbsoluteRange(Effect e, int playerid, int s_range, int o_range)
     设置target range属性并设置EFFECT_FLAG_ABSOLUTE_RANGE标志
        playerid != 0 s_range和o_range反转
    ●nil Effect.SetCountLimit(effect peffect, int v, [int code])
     void Effect.SetCountLimit(Effect e, int count[, int code=0])
     设置一回合可以发动的次数count（仅触发型效果有效），相同的code(不等于0或1时)共用1个次数
     code包含以下数值具有特殊的性质
     EFFECT_COUNT_CODE_OATH          誓约使用次数
     EFFECT_COUNT_CODE_DUEL          决斗中使用次数
     EFFECT_COUNT_CODE_SINGLE        同一张卡多个效果公共使用次数（不限制同名卡）
    ●nil Effect.SetReset(effect peffect, int v, [int c])
     void Effect.SetReset(Effect e, int reset_flag[, int reset_count=1])
     设置reset参数
    ●nil Effect.SetType(effect peffect, int v)
     void Effect.SetType(Effect e, int type)
     为效果e设置Type属性
    ●nil Effect.SetProperty(effect peffect, int v1, [int v2])
     void Effect.SetProperty(Effect e, int prop1[, int prop2])
     设置Property属性
    ●nil Effect.SetLabel(effect peffect, int v)
     void Effect.SetLabel(Effect e, int label)
     设置Label属性
    ●nil Effect.SetLabelObject(effect peffect, card|effect|group|nil p)
     void Effect.SetLabelObject(Effect e, Card|Group|Effect labelobject)
     设置LabelObject属性
    ●nil Effect.SetCategory(effect peffect, int v)
     void Effect.SetCategory(Effect e, int cate)
     设置Category属性
    ●nil Effect.SetHintTiming(effect peffect, int vs, [int vo])
     void Effect.SetHintTiming(Effect e, int s_time[, int o_time=s_time])
     设置提示时点
    ●nil Effect.SetCondition(effect peffect, function condition)
     void Effect.SetCondition(Effect e, function con_func)
     设置Condition属性
    ●nil Effect.SetTarget(effect peffect, function target)
     void Effect.SetTarget(Effect e, function targ_func)
     设置Target属性
    ●nil Effect.SetCost(effect peffect, function cost)
     void Effect.SetCost(Effect e, function cost_func)
     设置Cost属性
    ●nil Effect.SetValue(effect peffect, bool|function|number value)
     void Effect.SetValue(Effect e, function|int|bool val)
     设置Value属性
    ●nil Effect.SetOperation(effect peffect, function|nil operation)
     void Effect.SetOperation(Effect e, function op_func)
     设置Operation属性
    ●nil Effect.SetOwnerPlayer(effect peffect, [int p])
     void Effect.SetOwnerPlayer(Effect e[, int player])
     设置OwnerPlayer属性为player
    ●int Effect.GetDescription(effect peffect)
     int Effect.GetDescription(Effect e)
     返回效果描述
    ●int Effect.GetCode(effect peffect)
     int Effect.GetCode(Effect e)
     返回code属性
    ●int Effect.GetType(effect peffect)
     int Effect.GetType(Effect e)
     返回Type属性
    ●int Effect.GetProperty(effect peffect)
     int,int Effect.GetProperty(Effect e)
     返回Property属性
    ●int Effect.GetLabel(effect peffect)
     int Effect.GetLabel(Effect e)
     返回Label属性
    ●nil Effect.GetLabelObject(effect peffect)
     Card|Group|Effect Effect.GetLabelObject(Effect e)
     返回LabelObject属性
    ●int Effect.GetCategory(effect peffect)
     int Effect.GetCategory(Effect e)
     返回Category属性
    ●card Effect.GetOwner(effect peffect)
     Card Effect.GetOwner(Effect e)
     返回Owner属性
    ●card Effect.GetHandler(effect peffect)
     Card Effect.GetHandler(Effect e)
     返回效果在哪一张卡上生效(通常是用Card.RegisterEffect注册该效果的卡)
    ●function Effect.GetCondition(effect peffect)
     function Effect.GetCondition(Effect e)
     返回condition属性
    ●function Effect.GetTarget(effect peffect)
     function Effect.GetTarget(Effect e)
     返回target属性
    ●function Effect.GetCost(effect peffect)
     function Effect.GetCost(Effect e)
     返回cost属性
    ●function|int Effect.GetValue(effect peffect)
     function|int Effect.GetValue(Effect e)
     返回value属性
    ●function Effect.GetOperation(effect peffect)
     function Effect.GetOperation(Effect e)
     返回operation属性
    ●int Effect.GetActiveType(effect peffect)
     int Effect.GetActiveType(Effect e)
     返回e的效果类型（怪兽·魔法·陷阱）
     与发动该效果的卡的类型不一定相同，比如灵摆效果视为魔法卡的效果
    ●bool Effect.IsActiveType(effect peffect, int type)
     bool Effect.IsActiveType(Effect e, int type)
     检查e的效果类型（怪兽·魔法·陷阱）是否有type
    ●int Effect.GetOwnerPlayer(effect peffect)
     int Effect.GetOwnerPlayer(Effect e)
     返回OwnerPlayer属性，一般是Owner的控制者
    ●int Effect.GetHandlerPlayer(effect peffect)
     int Effect.GetHandlerPlayer(Effect e)
     返回当前者，一般是Handle的控制者
    ●bool Effect.IsHasProperty(effect peffect, int tflag1, [int tflag2])
     bool Effect.IsHasProperty(Effect e, int prop1[, int prop2])
     检查效果是否含有标志prop1[和prop2]
    ●bool Effect.IsHasCategory(effect peffect, int tcate)
     bool Effect.IsHasCategory(Effect e, int cate)
     检查效果是否含有效果分类cate
    ●bool Effect.IsHasType(effect peffect, int ttype)
     bool Effect.IsHasType(Effect e, int type)
     检查效果是否属于类型type
    ●bool Effect.IsActivatable(effect peffect, int playerid, [bool neglect_loc, bool neglect_target])
     bool Effect.IsActivatable(Effect e, int player)
     检查效果e能否由player发动
    ●bool Effect.IsActivated(effect peffect)
     bool Effect.IsActivated(Effect e)
     检查效果e能否是发动的效果（机壳）
    ●int Effect.GetActivateLocation(effect peffect)
     int Effect.GetActivateLocation(Effect e)
     返回效果e的发动区域
    ●int Effect.GetActivateSequence(effect peffect)
    ●bool Effect.CheckCountLimit(effect peffect, int p)
    ●nil Effect.UseCountLimit(effect peffect, int p, [int count, bool oath_only])
    ●group Group.CreateGroup()
     Group Group.CreateGroup()
     新建一个空的卡片组
    ●nil Group.KeepAlive(group pgroup)
     void Group.KeepAlive(Group g)
     让卡片组持续，把卡片组设置为效果的LabelObject需要设置
    ●nil Group.DeleteGroup(group pgroup)
     void Group.DeleteGroup(Group g)
     删除卡片组g
    ●group Group.Clone(group pgroup)
     Group Group.Clone(Group g)
     新建卡片组g的副本
    ●group Group.FromCards(nil|card pcard...)
     Group Group.FromCards(Card c[, ...])
     不定参数，把传入的所有卡组合成一个卡片组并返回
    ●nil Group.Clear(group pgroup)
     void Group.Clear(Group g)
     清空卡片组
    ●nil Group.AddCard(group pgroup, card pcard)
     void Group.AddCard(Group g, Card c)
     往g中增加c
    ●nil Group.RemoveCard(group pgroup, card pcard)
     void Group.RemoveCard(Group g, Card c)
     把c从g中移除
    ●nil|card Group.GetNext(group pgroup)
     Card Group.GetNext(Group g)
     使指针指向下一张卡并返回这张卡，如果不存在则返回nil
    ●nil|card Group.GetFirst(group pgroup)
     Card Group.GetFirst(Group g)
     返回g中第一张卡，并重置当前指针到g中第一张卡
     如果g中不存在卡则返回nil
    ●int Group.GetCount(group pgroup)
     int Group.GetCount(Group g)
     返回g中卡的数量
    ●nil Group.ForEach(group pgroup, function f)
     void Group.ForEach(Group g, function f)
     以g中的每一张卡作为参数调用一次f
    ●group Group.Filter(group pgroup, function ?, group|card pexception|pexgroup)
     Group Group.Filter(Group g, function f, Card ex|nil, ...)
     过滤函数，从g中筛选满足筛选条件f并且不等于ex的卡
     从第4个参数开始为额外参数
    ●int Group.FilterCount(group pgroup, function ?, group|card pexception|pexgroup)
     int Group.FilterCount(Group g, function f, Card ex|nil, ...)
     过滤函数，和Group.Filter基本相同，不同之处在于此函数只返回满足条件的卡的数量
    ●nil Group.FilterSelect(group pgroup, int playerid, function ?, int min, int max, group|card pexception|pexgroup)
     Group Group.FilterSelect(Group g, int player, function f, int min, int max, Card ex|nil, ...)
     过滤函数，让玩家player从g中选择min-max张满足筛选条件f并且不等于ex的卡
     从第7个参数开始为额外参数
    ●nil Group.Select(group pgroup, int playerid, int min, int max, group|card pexception|pexgroup)
     Group Group.Select(Group g, int player, int min, int max, Card ex|nil)
     让玩家player从g中选择min-max张不等于ex的卡
    ●nil Group.SelectUnselect(group pgroup1, group pgroup2, int playerid, [bool finishable, bool cancelable, int min, int max])
    ●nil Group.RandomSelect(group pgroup, int playerid, int count)
     Group Group.RandomSelect(Group g, int player, int count)
     让玩家player从g中随机选择count张卡
     因为是随机选择，所以参数player基本无用，由系统随机选取
    ●bool Group.IsExists(group pgroup, function ?, int count, group|card pexception|pexgroup)
     bool Group.IsExists(Group g, function f, int count, Card ex|nil, ...)
     过滤函数，检查g中是否存在至少count张满足筛选条件f并且不等于ex的卡
     从第5个参数开始为额外参数
    ●bool Group.CheckWithSumEqual(group pgroup, function ?, int acc, int min, int max)
     bool Group.CheckWithSumEqual(Group g, function f, int sum, int min, int max, ...)
     子集求和判定函数，f为返回一个interger值的函数
     检查g中是否存在一个数量为min-max的子集满足以f对子集的每一个元素求值的和等于sum，从第6个参数开始为额外参数
        比如：g:CheckWithSumEqual(Card.GetSynchroLevel,7,2,99)
        检查g中是否存在一个子集满足子集的同调用等级之和等于7
    ●group Group.SelectWithSumEqual(group pgroup, int playerid, function ?, int acc, int min, int max)
     Group Group.SelectWithSumEqual(Group g, int player, function f, int sum, int min, int max, ...)
     让玩家player从g中选取一个数量为min-max的子集使子集的特定函数的和等于sum，从第7个参数开始为额外参数
    ●bool Group.CheckWithSumGreater(group pgroup, function ?, int acc)
     bool Group.CheckWithSumGreater(Group g, function f, int sum, ...)
     子集求和判定函数之二，f为返回一个interger值的函数
     检查g中是否存在一个子集满足以f对子集的每一个元素求值的和刚好大于或者等于sum，从第4个参数开始为额外参数
     比如：g:CheckWithSumGreater(Card.GetRitualLevel,8)
        检查g中是否存在一个子集满足子集的仪式用等级之和大于等于8
        注：判定必须是“刚好”大于或者等于
        以等级为例，要使等级合计大于等于8，可以选择LV1+LV7而不可以选择LV1+LV4+LV4
    ●group Group.SelectWithSumGreater(group pgroup, int playerid, function ?, int acc)
     Group Group.SelectWithSumGreater(Group g, int player, function f, int sum, ...)
     让玩家player从g中选取一个子集使子集的特定函数f的和大于等于sum，从第5个参数开始为额外参数
    ●group|int Group.GetMinGroup(group pgroup, function ?)
     Group,int Group.GetMinGroup(Group g, function f, ...)
     f为返回一个interger值的函数，从g中筛选出具有最小的f的值的卡
     第2个返回值为这个最小值，从第3个参数开始为额外参数
     要使用第2个返回值注意检查g非空
    ●group|int Group.GetMaxGroup(group pgroup, function ?)
     Group,int Group.GetMaxGroup(Group g, function f, ...)
     f为返回一个interger值的函数，从g中筛选出具有最大的f的值的卡
     第2个返回值为这个最大值，从第3个参数开始为额外参数
     要使用第2个返回值注意检查g非空
    ●int Group.GetSum(group pgroup, function ?)
     int Group.GetSum(Group g, function f, ...)
     计算g中所有卡的取值的总和，f为为每张卡的取值函数，从第3个参数开始为额外参数
    ●int Group.GetClassCount(group pgroup, function ?)
     int Group.GetClassCount(Group g, function f, ...)
     计算g中所有卡的种类数量，f为分类的依据，返回相同的值视为同一种类，从第3个参数开始为额外参数
    ●nil Group.Remove(group pgroup, function ?, nil|card pexception)
     void Group.Remove(Group g, function f, Card ex|nil, ...)
     从g中移除满足筛选条件f并且不等于ex的所有卡，第4个参数开始是额外参数
    ●nil Group.Merge(group pgroup, group mgroup)
     void Group.Merge(Group g1, Group g2)
     把g2中的所有卡合并到g1
     注：g2本身不会发生变化
    ●nil Group.Sub(group pgroup, group sgroup)
     void Group.Sub(Group g1, Group g2)
     从g1中移除属于g2中的卡
     注：g2本身不会发生变化
    ●bool Group.Equal(group pgroup, group sgroup)
     bool Group.Equal(Group g1, Group g2)
     判断g1和g2是否相同
    ●bool Group.IsContains(group pgroup, card pcard)
     bool Group.IsContains(Group g, Card c)
     检查g中是否存在卡片c
    ●card Group.SearchCard(group pgroup, function ?)
     Card Group.SearchCard(Group g, function f, ...)
     过滤函数，返回g中满足筛选条件f的第一张卡，从第3个参数开始为额外参数
    ●int Group.GetBinClassCount(group pgroup, function ?)
    ●nil Duel.EnableGlobalFlag(int flag)
     void Duel.EnableGlobalFlag(int global_flag)
     设置全局标记global_flag
    ●int Duel.GetLP(int p)
     int Duel.GetLP(int player)
     返回玩家player的当前LP
    ●nil Duel.SetLP(int p, number lp)
     void Duel.SetLP(int player, int lp)
     设置玩家player的当前LP为lp
    ●int Duel.GetTurnPlayer()
     int Duel.GetTurnPlayer()
     返回当前的回合玩家
    ●int Duel.GetTurnCount(int playerid)
     int Duel.GetTurnCount([int player])
     返回[player所经过的]当前的回合数
    ●int Duel.GetDrawCount(int playerid)
     int Duel.GetDrawCount(int player)
     返回玩家player每回合的规则抽卡数量
    ●nil Duel.RegisterEffect(effect peffect, int playerid)
     void Duel.RegisterEffect(Effect e, int player)
     把效果e作为玩家player的效果注册给全局环境
    ●effect Duel.RegisterFlagEffect(int playerid, int code, int reset, int flag, int count, [int lab])
     Effect Duel.RegisterFlagEffect(int player, int code, int reset_flag, int property, int reset_count)
     为玩家player注册全局环境下的标识效果
     此效果总是影响玩家的(EFFECT_FLAG_PLAYER_TARGET)并且不会被无效化
     其余部分与Card.RegisterFlagEffect相同
    ●int Duel.GetFlagEffect(int playerid, int code)
     int Duel.GetFlagEffect(int player, int code)
     返回玩家player的特定的标识效果的数量
    ●nil Duel.ResetFlagEffect(int playerid, int code)
     void Duel.ResetFlagEffect(int player, int code)
     手动reset玩家player的特定的标识效果
    ●bool Duel.SetFlagEffectLabel(int playerid, int code, int lab)
    ●nil|int Duel.GetFlagEffectLabel(int playerid, int code)
    ●nil Duel.Destroy(group|card pcard|pgroup, int reason, [int dest])
     int Duel.Destroy(Card|Group targets, int reason[ ,int dest = LOCATION_GRAVE])
     以reason原因破坏targets去dest，返回值是实际被破坏的数量
     如果reason包含REASON_RULE，则破坏事件将不会检查卡片是否免疫效果，
     不会触发代破效果并且无视“不能破坏”
    ●nil Duel.Remove(group|card pcard|pgroup, int pos, int reason)
     int Duel.Remove(Card|Group targets, int pos, int reason)
     以reason原因，pos表示形式除外targets，返回值是实际被操作的数量
     如果reason包含REASON_TEMPORARY，那么视为是暂时除外，可以通过Duel.ReturnToField返回到场上
    ●nil Duel.SendtoGrave(group|card pcard|pgroup, int reason)
     int Duel.SendtoGrave(Card|Group targets, int reason)
     以reason原因把targets送去墓地，返回值是实际被操作的数量
    ●nil Duel.SendtoHand(group|card pcard|pgroup, nil|int playerid, int reason)
     int Duel.SendtoHand(Card|Group targets, int player|nil, int reason)
     以reason原因把targets送去玩家player的手牌，返回值是实际被操作的数量
     如果player是nil则返回卡的持有者的手牌
    ●nil Duel.SendtoDeck(group|card pcard|pgroup, nil|int playerid, int sequence, int reason)
     int Duel.SendtoDeck(Card|Group targets, int player|nil, int seq, int reason)
     以reason原因把targets送去玩家player的卡组，返回值是实际被操作的数量
     如果player是nil则返回卡的持有者的卡组
     如果seq=0，则是返回卡组最顶端；seq=1则是返回卡组最底端；
     其余情况则是返回最顶端并且标记需要洗卡组
    ●nil Duel.SendtoExtraP(group|card pcard|pgroup, nil|int playerid, int reason)
     int Duel.SendtoExtraP(Card|Group targets, int player|nil, int reason)
     以reason原因把灵摆卡targets送去玩家player的额外卡组，返回值是实际被操作的数量
     如果player是nil则返回卡的持有者的额外卡组
    ●group Duel.GetOperatedGroup()
     Group Duel.GetOperatedGroup()
     此函数返回之前一次卡片操作实际操作的卡片组包括
     Duel.Destroy, Duel.Remove, Duel.SendtoGrave, 
     Duel.SendtoHand, Duel.SendtoDeck, Duel.SendtoExtraP, Duel.Release, 
     Duel.ChangePosition, Duel.SpecialSummon, Duel.DiscardDeck
    ●nil Duel.Summon(int playerid, card pcard, bool ignore_count, nil|effect peffect, [int min_tribute, int zone])
     void Duel.Summon(int player, Card c, bool ignore_count, Effect e|nil[, min=0])
     让玩家以效果e对c进行通常召唤(非set)，至少使用min个祭品
     如果e=nil,那么就按照一般的通常召唤规则进行通常召唤
     如果ignore_count=true，则忽略每回合的通常召唤次数限制
    ●nil Duel.SpecialSummonRule(int playerid, card pcard, [int sumtype])
     void Duel.SpecialSummonRule(int player, Card c)
     让玩家player对c进行特殊召唤手续
    ●nil Duel.SynchroSummon(int playerid, card pcard, nil|card tuner, [group|nil mg])
     void Duel.SynchroSummon(int player, Card c, Card tuner[, Group mg])
     让玩家player以tuner作为调整[mg为素材]对c进行同调召唤手续
    ●nil Duel.XyzSummon(int playerid, card pcard, group|nil materials, [int minc, int maxc])
     void Duel.XyzSummon(int player, Card c, Group mg|nil[, min=0, max=0])
     让玩家player[从mg中][选min-max个素材]对c进行超量召唤手续
     mg非空且min为0则直接把mg全部作为超量素材
    ●nil Duel.MSet(int playerid, card pcard, bool ignore_count, nil|effect peffect, [int min_tribute, int zone])
     void Duel.MSet(int player, Card c, bool ignore_count, Effect e|nil[, min=0])
     让玩家以效果e对c进行通常召唤的Set，至少使用min个祭品
     如果e=nil,那么就按照一般的通常召唤规则进行通常召唤
     如果ignore_count=true，则忽略每回合的通常召唤次数限制
    ●nil Duel.SSet(int playerid, group|card pcard|pgroup, [int toplayer, bool confirm])
     void|int Duel.SSet(int player, Card|Group targets[, int target_player = player])
     让玩家player把targets放置到target_player的魔法陷阱区
     若targets为Group，则返回成功操作的数量
    ●bool|card Duel.CreateToken(int playerid, int code)
     Card Duel.CreateToken(int player, int code[, int setcode, int attack, inte defense, int level, int race, int attribute])
     以传入的参数数值新建一个Token并返回
    ●nil Duel.SpecialSummon(group|card pcard|pgroup, int sumtype, int sumplayer, int playerid, bool nocheck, bool nolimit, int positions, [int zone])
     int Duel.SpecialSummon(Card|Group targets, int sumtype, int sumplayer, int target_player, bool nocheck, bool nolimit, int pos)
     让玩家player以sumtype方式，pos表示形式把targets特殊召唤到target_player场上
     如果nocheck为true则无视卡的召唤条件如果nolimit为true则无视卡的苏生限制
     返回值是特殊召唤成功的卡的数量
    ●nil Duel.SpecialSummonStep(card pcard, int sumtype, int sumplayer, int playerid, bool nocheck, bool nolimit, int positions, [int zone])
     bool Duel.SpecialSummonStep(Card c, int sumtype, int sumplayer, int target_player, bool nocheck, bool nolimit, int pos)
     此函数是Duel.SpecialSummon的分解过程，只特殊召唤一张卡c
     此函数用于一个效果同时特殊召唤多张参数不同的卡
     此函数必须和Duel.SpecialSummonComplete一起使用
     返回值表示是否特殊召唤成功
    ●nil Duel.SpecialSummonComplete()
     void|int Duel.SpecialSummonComplete()
     此函数在确定复数个Duel.SpecialSummonStep调用完毕之后调用，用于触发事件
    ●bool Duel.IsCanAddCounter(int playerid, int countertype, int count, card pcard)
     bool Duel.IsCanAddCounter(int player, int countertype, int count, Card c)
     检查玩家player能否向卡片c添加count个countertype类型的指示物
    ●nil Duel.RemoveCounter(int rplayer, int s, int o, int countertype, int count, int reason)
     bool Duel.RemoveCounter(int player, int s, int o, int countertype, int count, int reason)
     让玩家player以reason为原因移除场上存在的countertype类型的count个指示物，返回值表示是否成功
     s表示对player来说的己方的可移除指示物的位置，o表示对player来说的对方的可移除指示物的位置
    ●bool Duel.IsCanRemoveCounter(int rplayer, int s, int o, int countertype, int count, int reason)
     bool Duel.IsCanRemoveCounter(int player, int s, int o, int countertype, int count, int reason)
     检查玩家player以reason为原因是否能移除场上的countertype类型的count个指示物
     s表示对player来说的己方的可移除指示物的位置，o表示对player来说的对方的可移除指示物的位置
    ●int Duel.GetCounter(int playerid, int s, int o, int countertype)
     int Duel.GetCounter(int player, int s, int o, int countertype)
     返回场上存在的countertype类型的指示物的数量
     s表示对player来说的己方的可移除指示物的位置，o表示对player来说的对方的可移除指示物的位置
    ●nil Duel.ChangePosition(group|card pcard|pgroup, int au, [int ad, int du, int dd, bool ?, bool ?])
     int Duel.ChangePosition(Card|Group targets, int au[, int ad=au, int du=au, int dd=au, bool noflip=false, bool setavailable=false])
     改变targets的表示形式返回实际操作的数量
     表侧攻击表示的变成au，里侧攻击表示的变成ad, 
     表侧守备表示变成du,里侧守备表示变成dd
     如果noflip=true则不触发反转效果（但会触发反转时的诱发效果）
     如果setavailable=true则对象之后变成里侧也发动反转效果
    ●nil Duel.Release(group|card pcard|pgroup, int reason)
     int Duel.Release(Card|Group targets, int reason)
     以reason原因解放targets返回值是实际解放的数量
     如果reason含有REASON_COST，则不会检查卡片是否不受效果影响
    ●nil Duel.MoveToField(card pcard, int move_player, int playerid, int destination, int positions, bool enable, [int zone])
     bool Duel.MoveToField(Card c, int move_player, int target_player, int dest, int pos, bool enabled)
     让玩家move_player把c移动的target_player的场上，返回值表示是否成功
     dest只能是LOCATION_MZONE或者LOCATION_SZONE，pos表示可选表示形式，enable表示是否立刻适用c的效果
    ●nil Duel.ReturnToField(card pcard, [int pos, int zone])
     bool Duel.ReturnToField(Card c[, int pos])
     把c以表示形式pos返回到场上，pos默认值是离场前的表示形式，返回值表示是否成功
     c必须是以REASON_TEMPORARY原因离场，并且离场后没有离开过那个位置
    ●nil Duel.MoveSequence(card pcard, int seq)
     void Duel.MoveSequence(Card c, int seq)
     移动c的序号，通常用于在场上换格子或者在卡组中移动到最上方或者最下方
    ●nil Duel.SwapSequence(card pcard1, card pcard2)
    ●nil Duel.Activate(effect peffect)
    ●nil Duel.SetChainLimit(function f)
     void Duel.SetChainLimit(function f)
     设定连锁条件，f的函数原型为 bool f(e,ep,tp)
     e表示要限制连锁的效果，ep表示要限制连锁的玩家，tp表示发动该效果的玩家
     在cost或者target处理中调用此函数可以限制可以连锁的效果的种类（如超融合）
     如果f返回false表示不能连锁，一旦设置连锁条件后发生了新的连锁那么连锁条件将会解除
    ●nil Duel.SetChainLimitTillChainEnd(function f)
     void Duel.SetChainLimitTillChainEnd(function f)
     功能同Duel.SetChainLimit，但是此函数设定的连锁条件直到连锁结束才会解除
    ●effect Duel.GetChainMaterial(int playerid)
     Effect Duel.GetChainMaterial(int player)
     返回玩家player受到的连锁素材的效果，此函数仅用于融合类卡的效果
    ●nil Duel.ConfirmDecktop(int playerid, int count)
     void Duel.ConfirmDecktop(int player, int count)
     确认玩家player卡组上方count张卡
    ●nil Duel.ConfirmExtratop(int playerid, int count)
    ●nil Duel.ConfirmCards(int playerid, group|card pcard|pgroup)
     void Duel.ConfirmCards(int player, Card|Group targets)
     给玩家player确认targets
    ●nil Duel.SortDecktop(int sort_player, int target_player, int count)
     void Duel.SortDecktop(int sort_player, int target_player, int count)
     让玩家sort_player对玩家target_player的卡组最上方count张卡进行排序
    ●bool|group|effect|int Duel.CheckEvent(int ev, [bool get_info])
     bool[,Group,int,int,Effect,int,int] Duel.CheckEvent(int event[, bool get_info])
     检查当前是否是event时点
     若get_info=true并且是正确的时点则还返回触发时点的信息 eg,ep,ev,re,r,rp
    ●nil Duel.RaiseEvent(group|card pcard|pgroup, int code, nil|effect peffect, int r, int rp, int ep, int ev)
     void Duel.RaiseEvent(Group|Card eg, int code, Effect re, int r, int rp, int ep, int ev)
     以eg,ep,ev,re,r,rp触发一个时点
    ●nil Duel.RaiseSingleEvent(card pcard, int code, nil|effect peffect, int r, int rp, int ep, int ev)
     void Duel.RaiseSingleEvent(Card ec, int code, Effect re, int r, int rp, int ep, int ev)
     以eg,ep,ev,re,r,rp为卡片ec触发一个单体时点
    ●bool Duel.CheckTiming(int tm)
     bool Duel.CheckTiming(int timing)
     检查当前是否是timing提示时点
    ●int Duel.GetEnvironment()
     int,int Duel.GetEnvironment()
     返回两个值，表示当前场地代号，以及当前场地效果的来源玩家
     场地代号指当前生效的场地卡的代号，或者海神的巫女把场地变化效果的值
     来源玩家指当前生效的场地卡的控制者，或者海神的巫女等卡的控制者
    ●bool Duel.IsEnvironment(int code, [int playerid, int loc])
     bool Duel.IsEnvironment(int code[, int player=PLAYER_ALL])
     检查玩家player是否为场地代号code的来源玩家
     场地代号指当前生效的场地卡的代号，或者海神的巫女把场地变化效果的值
     来源玩家指当前生效的场地卡的控制者，或者海神的巫女等卡的控制者
    ●nil Duel.Win(int playerid, int reason)
     void Duel.Win(int player, int win_reason)
     当前效果处理完令player以win_reason决斗胜利
    ●nil Duel.Draw(int playerid, int count, int reason)
     int Duel.Draw(int player, int count, int reason)
     让玩家player以原因reason抽count张卡，返回实际抽的卡的数量
     如果reason含有REASON_RULE则此次抽卡不受“不能抽卡”的效果的影响
    ●nil Duel.Damage(int playerid, number amount, int reason, [bool is_step])
     int Duel.Damage(int player, int value, int reason[, bool is_step=false])
     以reason原因给与玩家player造成value的伤害，返回实际收到的伤害值
     如果受到伤害变成回复等效果的影响时，返回值为0.
     is_step为true则是伤害/恢复LP过程的分解，需要调用Duel.RDComplete()触发时点
    ●nil Duel.Recover(int playerid, number amount, int reason, [bool is_step])
     int Duel.Recover(int player, int value, int reason[, bool is_step=false])
     以reason原因使玩家player回复value的LP，返回实际的回复值
     如果受到回复变成伤害等效果的影响时，返回值为0.
     is_step为true则是伤害/恢复LP过程的分解，需要调用Duel.RDComplete()触发时点
    ●nil Duel.RDComplete()
     void Duel.RDComplete()
     在调用Duel.Damage/Duel.Recover时，若is_step参数为true，则需调用此函数触发时点
    ●nil Duel.Equip(int playerid, card equip_card, card target, [bool up, bool step])
     bool Duel.Equip(int player, Card c1, Card c2[, bool up=true, bool is_step=false])
     把c1作为玩家player的装备卡装备给c2，返回值表示是否成功
     up=false则保持装备卡之前的表示形式
     is_step=true则是装备过程的分解，需要配合Duel.EquipComplete使用
    ●nil Duel.EquipComplete()
     void Duel.EquipComplete()
     在调用Duel.Equip时，若is_step参数为true，则需调用此函数触发时点
    ●nil Duel.GetControl(group|card pcard|pgroup, int playerid, [int reset_phase, int reset_count, int zone])
     bool Duel.GetControl(Card|Group targets, int player[, int reset_phase=0, int reset_count=0])
     让玩家player得到targets的控制权，返回值表示是否成功
    ●nil Duel.SwapControl(group|card pgroup1|pcard1, group|card pgroup2|pcard2, [int reset_phase, int reset_count])
     bool Duel.SwapControl(Card|Group targets1, Card|Group targets2[, int reset_phase=0, int reset_count=0])
     交换targets1与targets2的控制权，返回值表示是否成功
    ●bool Duel.CheckLPCost(int playerid, int cost)
     bool Duel.CheckLPCost(int player, int cost)
     检查玩家player是否能支付cost点lp
    ●nil Duel.PayLPCost(int playerid, int cost)
     void Duel.PayLPCost(int player, int cost)
     让玩家player支付cost点lp
    ●nil Duel.DiscardDeck(int playerid, int count, int reason)
     int Duel.DiscardDeck(int player, int count, int reason)
     以原因reason把玩家player的卡组最上端count张卡送去墓地，返回实际转移的数量
    ●int Duel.DiscardHand(int playerid, function|nil ?, int min, int max, int reason, [group|card pexception|pexgroup])
     int Duel.DiscardHand(int player, function f, int min, int max, int reason, Card ex|nil, ...)
     过滤函数让玩家player选择并丢弃满足筛选条件f兵不等于ex的min-max张手卡
     第7个参数开始为额外参数
    ●nil Duel.DisableShuffleCheck(bool disable)
     void Duel.DisableShuffleCheck([disable=true])
     使下一个操作不检查是否需要洗切卡组或手卡
     注：如果不调用此函数，
     除了调用Duel.DiscardDeck和Duel.Draw之外从卡组中取出卡或者把卡加入手卡
     或者把卡加入卡组（非最上端或最底端）时，系统会自动在效果处理结束时洗切卡组或手卡
     如果不希望如此，比如从卡组顶端除外一张卡等操作，那么需要调用此函数
     此函数仅保证紧接着的一次操作不会进行洗卡检测
    ●nil Duel.ShuffleDeck(int playerid)
     void Duel.ShuffleDeck(int player)
     手动洗切玩家player的卡组
     注：会重置洗卡检测的状态
    ●nil Duel.ShuffleExtra(int playerid)
    ●nil Duel.ShuffleHand(int playerid)
     void Duel.ShuffleHand(int player)
     手动洗切玩家player的手卡
     注：会重置洗卡检测的状态
    ●nil Duel.ShuffleSetCard(group pgroup)
     void Duel.ShuffleSetCard(Group g)
     洗切覆盖在怪兽区域的卡（魔术礼帽）
    ●nil Duel.ChangeAttacker(card attacker, [bool ignore_count])
     void Duel.ChangeAttacker(Card c)
     将攻击怪兽变为c
     注：此函数会使原来的攻击怪兽视为攻击过
    ●bool Duel.ChangeAttackTarget(nil|card target)
     bool Duel.ChangeAttackTarget(Card c|nil)
     将攻击对象变为c，c为nil表示直接攻击，返回值表示是否成功转移攻击对象
    ●nil Duel.CalculateDamage(card attacker, nil|card attack_target, [bool new_attack])
     void Duel.CalculateDamage(Card c1, Card c2)
     令c1与c2进行战斗伤害计算
    ●int Duel.GetBattleDamage(int playerid)
     int Duel.GetBattleDamage(int player)
     返回玩家player在本次战斗中受到的伤害
    ●nil Duel.ChangeBattleDamage(int playerid, int dam, [bool check])
     void Duel.ChangeBattleDamage(int player, int value[, bool check=true])
     把玩家player在本次战斗中受到的伤害变成value，check为false则原本战斗伤害为0也改变伤害
    ●nil Duel.ChangeTargetCard(int count, group pgroup)
     void Duel.ChangeTargetCard(int chainc, Group g)
     把连锁chainc的对象换成g
    ●nil Duel.ChangeTargetPlayer(int count, int playerid)
     void Duel.ChangeTargetPlayer(int chainc, in player)
     把连锁chainc的对象玩家换成player
    ●nil Duel.ChangeTargetParam(int count, int param)
     void Duel.ChangeTargetParam(int chainc, int param)
     把连锁chainc的参数换成param
    ●nil Duel.BreakEffect()
     void Duel.BreakEffect()
     中断当前效果，使之后的效果处理视为不同时处理，此函数会造成错时点
    ●nil Duel.ChangeChainOperation(int count, function pf)
     void Duel.ChangeChainOperation(int chainc, function f)
     把连锁chainc的效果的处理函数换成f，用于实现“把效果变成”等的效果
    ●bool Duel.NegateActivation(int c)
     bool Duel.NegateActivation(int chainc)
     使连锁chainc的发动无效，返回值表示是否成功
    ●bool Duel.NegateEffect(int c)
     bool Duel.NegateEffect(int chainc)
     使连锁chainc的效果无效，返回值表示是否成功
    ●nil Duel.NegateRelatedChain(card pcard, int reset_flag)
     void Duel.NegateRelatedChain(Card c, int reset)
     使卡片c的已经发动的连锁都无效化，发生reset事件则重置
    ●nil Duel.NegateSummon(group|card pcard|pgroup)
     void Duel.NegateSummon(Card|Group targets)
     使正在召唤·反转召唤·特殊召唤的targets的召唤无效
    ●nil Duel.IncreaseSummonedCount(card pcard)
     void Duel.IncreaseSummonedCount([Card c])
     手动消耗1次玩家[对于卡片c]的通常召唤的次数
    ●bool Duel.CheckSummonedCount(card pcard)
     bool Duel.CheckSummonedCount([Card c])
     检查回合玩家本回合是否还能通常召唤[卡片c]
    ●int Duel.GetLocationCount(int playerid, int location, [nil|int uplayer, int reason, int zone])
     int Duel.GetLocationCount(int player, int location[, int use_player, int reason = LOCATION_REASON_TOFIELD])
     返回玩家player的场上location可用的空格数
     location只能是LOCATION_MZONE或者LOCATION_SZONE
     reason为LOCATION_REASON_TOFIELD或LOCATION_REASON_CONTROL
     ##额外参数与凯撒斗技场的效果有关
    ●int Duel.GetMZoneCount(int playerid, [group|nil|card mcard|mgroup, int uplayer, int reason, int zone])
    ●int Duel.GetLocationCountFromEx(int playerid, [int uplayer, group|nil|card mcard|mgroup, card scard, int zone])
    ●int Duel.GetUsableMZoneCount(int playerid, [int uplayer])
    ●group Duel.GetLinkedGroup(int rplayer, int s, int o)
    ●int Duel.GetLinkedGroupCount(int rplayer, int s, int o)
    ●int Duel.GetLinkedZone(int playerid)
    ●card Duel.GetFieldCard(int playerid, int location, int sequence)
     Card Duel.GetFieldCard(int player, int location, int seq)
     返回玩家player的场上位于location序号为seq的卡，常用于获得场地区域·灵摆区域的卡
    ●bool Duel.CheckLocation(int playerid, int location, int sequence)
     bool Duel.CheckLocation(int player, int location, int seq)
     检查玩家player的场上位于location序号为seq的空格是否可用
    ●int Duel.GetCurrentChain()
     int Duel.GetCurrentChain()
     返回当前正在处理的连锁序号
    ●group|nil|effect|int Duel.GetChainInfo(int c, [int flag])
     ... Duel.GetChainInfo(int chainc, ...)
     返回连锁chainc的信息，如果chainc=0，则返回当前正在处理的连锁的信息
     此函数根据传入的参数个数按顺序返回相应数量的返回值参数可以是:
     CHAININFO_CHAIN_COUNT               连锁序号
     CHAININFO_TRIGGERING_EFFECT         连锁的效果
     CHAININFO_TRIGGERING_PLAYER         连锁的玩家
     CHAININFO_TRIGGERING_CONTROLER      连锁发生位置所属玩家
     CHAININFO_TRIGGERING_LOCATION       连锁发生位置
     CHAININFO_TRIGGERING_SEQUENCE       连锁发生的位置的序号
     CHAININFO_TARGET_CARDS              连锁的对象卡片组
     CHAININFO_TARGET_PLAYER             连锁的对象玩家
     CHAININFO_TARGET_PARAM              连锁的对象参数
     CHAININFO_DISABLE_REASON            连锁被无效的原因效果
     CHAININFO_DISABLE_PLAYER            连锁被无效的原因玩家
     CHAININFO_CHAIN_ID                  连锁的唯一标识
     CHAININFO_TYPE                      连锁卡片的类型（怪兽·魔法·陷阱）
     CHAININFO_EXTTYPE                   连锁卡片的具体类型（例如同调怪兽·永续魔法·反击陷阱）
     举例：
     Duel.GetChainInfo(0,CHAININFO_TRIGGERING_LOCATION,CHAININFO_TARGET_CARDS)
     将会返回当前连锁发生的位置和对象卡
    ●group|effect|int Duel.GetChainEvent(int count)
    ●card Duel.GetFirstTarget()
     Card,... Duel.GetFirstTarget()
     返回连锁的所有的对象卡，一般只有一个对象时使用
    ●int Duel.GetCurrentPhase()
     int Duel.GetCurrentPhase()
     返回当前的阶段
    ●nil Duel.SkipPhase(int playerid, int phase, int reset, int count, [int value])
     void Duel.SkipPhase(int player, int phase, int reset_flag, int reset_count[, int value])
     跳过玩家player的phase阶段，并在特定的阶段后reset，reset参数和效果相同
     #value只对phase=PHASE_BATTLE才有用，value=1跳过战斗阶段的结束步骤，用于“变成回合结束阶段”等（招财猫王，闪光弹）
    ●bool Duel.IsDamageCalculated()
     bool Duel.IsDamageCalculated()
     用于在伤害阶段检查是否已经计算了战斗伤害
    ●card Duel.GetAttacker()
     Card Duel.GetAttacker()
     返回此次战斗攻击的卡
    ●card Duel.GetAttackTarget()
     Card|nil Duel.GetAttackTarget()
     返回此次战斗被攻击的卡，如果返回nil表示是直接攻击
    ●nil Duel.NegateAttack()
     bool Duel.NegateAttack()
     无效此次攻击，返回值表示是否成功
     此次攻击已经被其他效果无效或导致攻击的卡不能攻击则返回false
    ●nil Duel.ChainAttack(card core.chain_attack_target)
     void Duel.ChainAttack([Card c])
     使攻击卡[或卡片c]可以再进行1次攻击（开辟，破灭的女王）
    ●nil Duel.Readjust()
     void Duel.Readjust()
     刷新场上的卡的信息
     非特定情况或者不清楚原理请勿使用此函数以免形成死循环
    ●nil Duel.AdjustInstantly(card pcard)
     void Duel.AdjustInstantly([Card c])
     手动刷新场上[受到卡片c影响]的卡的无效状态
    ●group Duel.GetFieldGroup(int playerid, int location1, int location2)
     Group Duel.GetFieldGroup(int player, int s, int o)
     返回指定位置的卡
    ●int Duel.GetFieldGroupCount(int playerid, int location1, int location2)
     int Duel.GetFieldGroupCount(int player, int s, int o)
     返回指定位置的卡的数量
    ●group Duel.GetDecktopGroup(int playerid, int count)
     Group Duel.GetDecktopGroup(int player, int count)
     返回玩家player的卡组最上方的count张卡
    ●group Duel.GetExtraTopGroup(int playerid, int count)
    ●group Duel.GetMatchingGroup(function|nil ?, int self, int location1, int location2, group|card pexception|pexgroup)
     Group Duel.GetMatchingGroup(function f, int player, int s, int o, Card ex|nil, ...)
     过滤函数，返回指定位置满足过滤条件f并且不等于ex的卡
     第6个参数开始为额外参数
    ●int Duel.GetMatchingGroupCount(function|nil ?, int self, int location1, int location2, group|card pexception|pexgroup)
     int Duel.GetMatchingGroupCount(function f, int player, int s, int o, Card ex|nil, ...)
     过滤函数，返回指定位置满足过滤条件f并且不等于ex的卡的数量
    ●nil|card Duel.GetFirstMatchingCard(function|nil ?, int self, int location1, int location2, group|card pexception|pexgroup)
     Card Duel.GetFirstMatchingCard(function f, int player, int s, int o, Card ex|nil, ...)
     过滤函数，返回指定位置满足过滤条件f并且不等于ex的第一张卡
     第6个参数开始为额外参数
    ●bool Duel.IsExistingMatchingCard(function|nil ?, int self, int location1, int location2, int fcount, group|card pexception|pexgroup)
     bool Duel.IsExistingMatchingCard(function f, int player, int s, int o, int count, Card ex|nil, ...)
     过滤函数，检查指定位置是否存在至少count张满足过滤条件f并且不等于ex的卡
     第7个参数开始为额外参数
    ●nil Duel.SelectMatchingCard(int playerid, function|nil ?, int self, int location1, int location2, int min, int max, group|card pexception|pexgroup)
     Group Duel.SelectMatchingCard(int sel_player, function f, int player, int s, int o, int min, int max, Card ex|nil, ...)
     过滤函数，让玩家sel_player选择指定位置满足过滤条件f并且不等于ex的min-max张卡
     第9个参数开始为额外参数
    ●group Duel.GetReleaseGroup(int playerid, [bool hand])
     Group Duel.GetReleaseGroup(int player[, bool use_hand=false])
     返回玩家player可解放（非上级召唤用）的卡片组，use_hand为true则包括手卡
    ●int Duel.GetReleaseGroupCount(int playerid, [bool hand])
     integer Duel.GetReleaseGroupCount(int player[, bool use_hand=false])
     返回玩家player可解放（非上级召唤用）的卡片数量，use_hand为true则包括手卡
    ●bool Duel.CheckReleaseGroup(int playerid, function|nil ?, int fcount, group|card pexception|pexgroup)
     bool Duel.CheckReleaseGroup(int player, function f, int count, Card ex|nil, ...)
     检查玩家player场上是否存在至少count张满足过滤条件f并且不等于ex的可解放的卡（非上级召唤用）
     第5个参数开始为额外参数
    ●nil Duel.SelectReleaseGroup(int playerid, function|nil ?, int min, int max, group|card pexception|pexgroup)
     Group Duel.SelectReleaseGroup(int sel_player, function f, int min, int max, Card ex|nil, ...)
     过滤函数，让玩家player从场上选择min-max张不等于ex的满足条件f的可解放的卡（非上级召唤用）
    ●bool Duel.CheckReleaseGroupEx(int playerid, function|nil ?, int fcount, group|card pexception|pexgroup)
     bool Duel.CheckReleaseGroupEx(int player, function f, int count, Card ex|nil, ...)
     检查玩家player场上·手卡是否存在至少count张满足过滤条件f并且不等于ex的可解放的卡（非上级召唤用）
    ●nil Duel.SelectReleaseGroupEx(int playerid, function|nil ?, int min, int max, group|card pexception|pexgroup)
     Group Duel.SelectReleaseGroupEx(int player, function f, int min, int max, Card ex|nil, ...)
     过滤函数，让玩家player从场上·手卡选择min-max张不等于ex的满足条件f的可解放的卡（非上级召唤用）
    ●group Duel.GetTributeGroup(card target)
     Group Duel.GetTributeGroup(Card c)
     返回用于通常召唤c可解放（上级召唤用）的卡片组
    ●int Duel.GetTributeCount(card target, [group|nil mg, bool ex])
     int Duel.GetTributeCount(Card c[, Group mg, bool ex=false])
     返回[mg中]用于通常召唤c的祭品数量，ex=true则允许对方场上的怪兽（太阳神之翼神龙-球体形）
     此数量不一定等于Duel.GetTributeGroup的返回值中的卡片数量
     因为某些卡可以作为两个祭品来使用
    ●bool Duel.CheckTribute(card target, int min, [nil|int max, group|nil mg, nil|int toplayer, nil|int zone])
     Group Duel.CheckTribute(Card c, int min[, int max, Group mg, int toplayer])
     [为了召唤到toplayer场上，]判断[在mg中]是否存在用于通常召唤c的min[到max]个祭品
    ●nil Duel.SelectTribute(int playerid, card target, int min, int max, [group|nil mg, int toplayer])
     Group Duel.SelectTribute(int player, Card c, int min, int max[, Group mg, bool ex=false])
     让玩家player[从mg中]选择用于通常召唤c的min-max个祭品，ex=true则允许对方场上的怪兽（太阳神之翼神龙-球体形）
    ●int Duel.GetTargetCount(function|nil ?, int self, int location1, int location2, group|card pexception|pexgroup)
     int Duel.GetTargetCount(function f, int player, int s, int o, Card ex|nil, ...)
     基本同Duel.GetMatchingGroupCount，不同之处在于需要追加判定卡片是否能成为当前正在处理的效果的对象
    ●bool Duel.IsExistingTarget(function|nil ?, int self, int location1, int location2, int count, group|card pexception|pexgroup)
     bool Duel.IsExistingTarget(function f, int player, int s, int o, int count, Card ex|nil, ...)
     过滤函数，检查指定位置是否存在至少count张满足过滤条件f并且不等于ex
     并且可以成为当前正在处理的效果的对象的卡
     第7个参数开始为额外参数
    ●nil Duel.SelectTarget(int playerid, function|nil ?, int self, int location1, int location2, int min, int max, group|card pexception|pexgroup)
     Group Duel.SelectTarget(int sel_player, function f, int player, int s, int o, int min, int max, Card ex|nil, ...)
     过滤函数，让玩家sel_player选择指定位置满足过滤条件f并且不等于ex
     并且可以成为当前正在处理的效果的对象的min-max张卡
     第9个参数开始为额外参数
     此函数会同时将当前正在处理的连锁的对象设置成选择的卡
    ●nil Duel.SelectFusionMaterial(int playerid, card pcard, group pgroup, [nil|card cg, int chkf])
     Group Duel.SelectFusionMaterial(int player, Card c, Group g[, Card gc|nil, int chkf=PLAYER_NONE])
     让玩家player从g中选择一组[必须包含gc在内的]融合怪兽c的融合素材
     ##根据c的种类为EFFECT_FUSION_MATERIAL的效果的Operation操作
    ●nil Duel.SetFusionMaterial(group pgroup)
     void Duel.SetFusionMaterial(Group g)
     设置g为需要使用的融合素材
    ●nil Duel.SetSynchroMaterial(group pgroup)
     void Duel.SetSynchroMaterial(Group g)
     设置g为需要使用的同调素材
    ●int Duel.SelectSynchroMaterial(int playerid, card pcard, function|nil ?, function|nil ?, int min, int max, [nil|card smat, group|nil mg])
     Group Duel.SelectSynchroMaterial(int player, Card c, function f1, function f2, int min, int max[, Card smat, Group mg])
     让玩家player[从mg中]选择用于同调c需要的[必须包含smat在内（如果有mg~=nil则忽略此参数）]满足条件的数量为min-max的一组素材
     f1是调整需要满足的过滤条件，f2是调整以外的部分需要满足的过滤条件
    ●bool|int Duel.CheckSynchroMaterial(card pcard, function|nil ?, function|nil ?, int min, int max, [nil|card smat, group|nil mg])
     bool Duel.CheckSynchroMaterial(Card c, function f1, function f2, int min, int max[, Card smat, Group mg])
     检查[mg中]是否存在一组[必须包括smat在内的]满足条件的min-max张卡作为同调召唤c的素材
     f1是调整需要满足的过滤条件，f2是调整以外的部分需要满足的过滤条件
    ●int Duel.SelectTunerMaterial(int playerid, card pcard, card tuner, function|nil ?, function|nil ?, int min, int max, [group|nil mg])
     Group Duel.SelectTunerMaterial(int player, Card c, Card tuner, function f1, function f2, int min, int max[, Group mg])
     让玩家[从mg中]选择用于同调c需要的满足条件的以tuner作为调整的min-max张卡的一组素材
     f1是调整需要满足的过滤条件，f2是调整以外的部分需要满足的过滤条件
    ●bool|int Duel.CheckTunerMaterial(card pcard, card tuner, function|nil ?, function|nil ?, int min, int max, [group|nil mg])
     bool Duel.CheckTunerMaterial(Card c, Card tuner, function f1, function f2, int min, int max[, Group mg])
     检查以tuner作为调整[在mg中]是否存在一组满足条件的min-max张卡作为同调召唤c的素材
     f1是调整需要满足的过滤条件，f2是调整以外的部分需要满足的过滤条件
    ●group Duel.GetRitualMaterial(int playerid)
     Group Duel.GetRitualMaterial(int player)
     返回玩家player可用的用于仪式召唤素材的卡片组
     包含手上，场上可解放的以及墓地的仪式魔人等卡
    ●nil Duel.ReleaseRitualMaterial(group pgroup)
     void Duel.ReleaseRitualMaterial(Group g)
     解放仪式用的素材g，如果是墓地的仪式魔人等卡则除外
    ●group Duel.GetFusionMaterial(int playerid)
     Group Duel.GetFusionMaterial(int player)
     返回玩家player可用的用于融合召唤素材的卡片组
     包含手卡·场上的怪兽的以及万溶炼金术师的装备卡
    ●nil Duel.SetSelectedCard(group|card pcard|pgroup)
     void Duel.SetSelectedCard(Card|Group cards)
     将cards设置为Group.SelectWithSumEqual或Group.SelectWithSumGreater已选择的卡片，
    ●group Duel.GrabSelectedCard()
    ●nil Duel.SetTargetCard(group|card pcard|pgroup)
     void Duel.SetTargetCard(Card|Group targets)
     把当前正在处理的连锁的对象设置成targets
     注，这里的对象指的的广义的对象，包括不取对象的效果可能要处理的对象
    ●nil Duel.ClearTargetCard()
     void Duel.ClearTargetCard()
     把当前正在处理的连锁的对象全部清除
    ●nil Duel.SetTargetPlayer(int playerid)
     void Duel.SetTargetPlayer(int player)
     把当前正在处理的连锁的对象玩家设置成player
    ●nil Duel.SetTargetParam(int param)
     void Duel.SetTargetParam(integer)
     void Duel.SetTargetParam(inte param)
     把当前正在处理的连锁的对象参数设置成param
    ●nil Duel.SetOperationInfo(int ct, int cate, group|card pcard|pgroup, int count, int playerid, int param)
     void Duel.SetOperationInfo(int chainc, int category, Card|Group targets, int count, int target_player, int target_param)
     设置当前处理的连锁的操作信息此操作信息包含了效果处理中确定要处理的效果分类
     比如潜行狙击手需要设置CATEGORY_DICE，但是不能设置CATEGORY_DESTROY，因为不确定
     对于破坏效果，targets需要设置成发动时可能成为连锁的影响对象的卡，
     并设置count为发动时确定的要处理的卡的数量
     比如黑洞发动时，targets需要设定为场上的所有怪兽，count设置成场上的怪的数量
     对于需要移动卡片位置的CATEGORY_SPECIAL_SUMMON,CATEGORY_TOHAND,CATEGORY_TODECK等分类，
     如果要处理的卡是确定的（比如取对象），则设置targets为这些卡，count为数量，
     如果要处理的卡是不确定的（效果处理时才能确定，一般是不取对象的效果），
        则设置targets为nil，count为预计要处理的卡的数量，
        target_player为预计要处理的卡的持有者（不确定就为0）
        target_param为预计要处理的卡的位置
     例如增援：SetOperationInfo(0,CATEGORY_TOHAND,nil,1,tp,LOCATION_DECK)
     操作信息用于很多效果的发动的检测，例如星尘龙，王家长眠之谷等
    ●bool|group|nil|int Duel.GetOperationInfo(int ct, int cate)
     bool,Card|Group,int,int,int Duel.GetOperationInfo(int chainc, int category)
     返回连锁chainc的category分类的操作信息，返回值为5个，
     第一个返回值是false的话表示不存在该分类
     后4个返回值对应Duel.SetOperationInfo的后4个参数：Card|Group targets, int count, int target_player, int target_param
    ●int Duel.GetOperationCount(int ct)
     int Duel.GetOperationCount(int chainc)
     返回连锁chainc包含的操作分类的数量
    ●bool Duel.CheckXyzMaterial(card scard, function|nil ?, int lv, int minc, int maxc, group|nil mg)
     bool Duel.CheckXyzMaterial(Card c, function f, int lv, int min, int max, Group mg|nil)
     检查场上或mg中是否存在超量召唤c的超量用等级为lv的min-max个满足条件f的叠放素材
    ●nil Duel.SelectXyzMaterial(int playerid, card scard, function|nil ?, int lv, int minc, int maxc, [group|nil mg])
     Group Duel.SelectXyzMaterial(int player, Card c, function f, int lv, int min, int max[, Group mg])
     让玩家player为超量怪兽c[从mg中]选择超量用等级为lv的min-max个满足条件f的叠放素材
    ●nil Duel.Overlay(card target, group|card pcard|pgroup)
     void Duel.Overlay(Card c, Card|Group ocard)
     把ocard作为c的叠放卡叠放
    ●group Duel.GetOverlayGroup(int rplayer, int s, int o)
     Group Duel.GetOverlayGroup(int player, int s, int o)
     返回指定位置的所有叠放的卡
    ●int Duel.GetOverlayCount(int rplayer, int s, int o)
     int Duel.GetOverlayCount(int player, int s, int o)
     返回指定位置的所有叠放的卡的数量
    ●bool Duel.CheckRemoveOverlayCard(int playerid, int s, int o, int count, int reason)
     bool Duel.CheckRemoveOverlayCard(int player, int s, int o, int count, int reason)
     检查player能否以原因reason移除指定位置至少count张卡
    ●nil Duel.RemoveOverlayCard(int playerid, int s, int o, int min, int max, int reason)
     bool Duel.RemoveOverlayCard(int player, int s, int o, int min, int max, int reason)
     让player以reason原因移除指定位置的min-max张叠放卡，返回值表示是否成功
    ●nil Duel.Hint(int htype, int playerid, int desc)
     void Duel.Hint(int hint_type, int player, int desc)
     给玩家player发送hint_type类型的消息提示，提示内容为desc
     #hint_type只能为以下类型：
     #HINT_SELECTMSG	将提示内容写入缓存，用于选择卡片的提示，例如Duel.SelectMatchingCard等
     #HINT_OPSELECTED	向player提示“对方选择了：...”，常用于向对方玩家提示选择发动了什么效果
     #HINT_CARD		此时desc应为卡号，手动显示卡片发动的动画，常用于提示不入连锁的处理
     #HINT_RACE		此时desc应为种族，向player提示“对方宣言了：...”种族
     #HINT_ATTRIB		此时desc应为属性，向player提示“对方宣言了：...”属性
     #HINT_CODE		此时desc应为卡号，向player提示“对方宣言了：...”卡片
     #HINT_NUMBER		此时desc视为单纯的数字，向player提示“对方选择了：...”数字
     #HINT_MESSAGE	弹出一个对话框显示信息
     #HINT_EVENT		将提示内容写入缓存，用于时点的提示信息（诱发即时效果的提示）
     #HINT_EFFECT		同HINT_CARD
    ●nil Duel.HintSelection(group pgroup)
     void Duel.HintSelection(Group g)
     手动为g显示被选为对象的动画效果，并记录这些卡被选为对象
    ●nil Duel.SelectEffectYesNo(int playerid, card pcard, [int desc])
     bool Duel.SelectEffectYesNo(int player, Card c)
     让玩家player选择是否发动卡片c的效果
    ●nil Duel.SelectYesNo(int playerid, int desc)
     bool Duel.SelectYesNo(int player, int desc)
     让玩家player选择是或否
    ●nil Duel.SelectOption(int playerid, [int ?...])
     int Duel.SelectOption(int player, int desc1, ...)
     让玩家选择选项，从第二个参数开始，每一个参数代表一条选项
     返回选择的选项的序号(从0开始)
    ●nil Duel.SelectSequence()
     void Duel.SelectSequence()
     #(预留）
    ●nil Duel.SelectPosition(int playerid, card pcard, int positions)
     int Duel.SelectPosition(int player, Card c, int pos)
     让玩家player选择c的表示形式并返回
    ●nil Duel.SelectDisableField(int playerid, int count, int location1, int location2, int filter)
     int Duel.SelectDisableField(int player, int count, int s, int o, int filter)
     让玩家player选择指定位置满足标记条件filter的count个可用的空格，并返回选择位置的标记
     常用于选择区域不能使用或移动怪兽格子
     ##位置标记的定义如下
     ##flag = 0;
     ##seq为在玩家p，位置l中选择的格子序号
     ##for(int32 i = 0; i < count; ++i) {
     ##	flag |= 1 << (seq[i] + (p[i] == player ? 0 : 16) + (l[i] == LOCATION_MZONE ? 0 : 8));
     ##}
    ●nil Duel.AnnounceRace(int playerid, int count, int available)
     int Duel.AnnounceRace(int player, int count, int available)
     让玩家player从可选的种族中宣言count个种族
     available是所有可选种族的组合值
    ●nil Duel.AnnounceAttribute(int playerid, int count, int available)
     int Duel.AnnounceAttribute(int player, int count, int available)
     让玩家player从可选的属性中宣言count个属性
     available是所有可选属性的组合值
    ●nil Duel.AnnounceLevel(int playerid, [nil|int min, nil|int max, int ?...])
     int Duel.AnnounceLevel(int player)
     让玩家宣言一个等级
    ●nil Duel.AnnounceCard(int playerid, [int ttype])
     int Duel.AnnounceCard(int player[, int type=TYPE_MONSTER+TYPE_SPELL+TYPE_TRAP])
     让玩家player宣言一个[type类型的]卡片代号
    ●nil Duel.AnnounceCardFilter(int playerid, int ?...)
     int Duel.AnnounceCardFilter(int player, ...)
     让玩家player宣言一个满足条件的卡片代号，条件用后缀表达式...表示
    ●nil Duel.AnnounceType(int playerid)
     int Duel.AnnounceType(int player)
     让玩家player宣言一个卡片类型
    ●nil Duel.AnnounceNumber(int playerid, int ?...)
     int,int Duel.AnnounceNumber(int player, int number, ...)
     让玩家player宣言一个数字
     从第二个参数开始，每一个参数代表一个可宣言的数字
     第一个返回值的宣言的数字，第二个返回值是宣言数字在所有选项中的位置
    ●nil Duel.AnnounceCoin(int playerid)
     int Duel.AnnounceCoin(int player)
     让玩家player宣言硬币的正反面
    ●nil Duel.TossCoin(int playerid, int count)
     ... Duel.TossCoin(int player, int count)
     让玩家player投count(<=5)次硬币，返回值为count个结果，0或者1.
    ●nil Duel.TossDice(int playerid, int count1, [int count2])
     ... Duel.TossDice(int player, int count1[, int count2 = 0])
     让玩家player投count1次骰子[，1-player投count2次骰子](count1+count2<=5)
     返回值为count1+count2个结果，1-6
    ●nil Duel.RockPaperScissors(bool repeat)
    ●int Duel.GetCoinResult()
     int,int,int,int,int Duel.GetCoinResult()
     返回当前投硬币的结果
    ●int Duel.GetDiceResult()
     int,int,int,int,int Duel.GetDiceResult()
     返回当前掷骰子的结果
    ●nil Duel.SetCoinResult(int res...)
     void Duel.SetCoinResult(int res, ... )
     强行修改投硬币的结果为res
     此函数用于永续的EVENT_TOSS_COIN事件中
    ●nil Duel.SetDiceResult(int res...)
     void Duel.SetDiceResult(int res, ...)
     强行修改投骰子的结果为res
     此函数用于永续的EVENT_TOSS_DICE事件中
    ●nil|effect Duel.IsPlayerAffectedByEffect(int playerid, int code)
     Effect|nil Duel.IsPlayerAffectedByEffect(int player, int code)
     检查player是否受到种类为code的效果影响，如果有就返回该效果
    ●bool Duel.IsPlayerCanDraw(int playerid, [int count])
     bool Duel.IsPlayerCanDraw(int player[, int count=0])
     检查玩家player是否可以效果抽[count张]卡
    ●bool Duel.IsPlayerCanDiscardDeck(int playerid, int count)
     bool Duel.IsPlayerCanDiscardDeck(int player, int count)
     检查玩家player是否可以把卡组顶端count张卡送去墓地
    ●bool Duel.IsPlayerCanDiscardDeckAsCost(int playerid, int count)
     bool Duel.IsPlayerCanDiscardDeckAsCost(int player, int count)
     检查玩家player能否把卡组顶端count张卡送去墓地作为cost
    ●bool Duel.IsPlayerCanSummon(int playerid, int sumtype, card pcard)
     bool Duel.IsPlayerCanSummon(int player[, int sumtype, Card c])
     检查玩家player是否可以通常召唤[c，以sumtype方式]
     如果需要可选参数，则必须全部使用
     仅当玩家收到“不能上级召唤”等效果的影响时返回false
    ●bool Duel.IsPlayerCanSpecialSummon(int playerid, int sumtype, int sumpos, int toplayer, card pcard)
     bool Duel.IsPlayerCanSpecialSummon(int player[, int sumtype, int sumpos, int target_player, Card c])
     检查玩家player能否特殊召唤[c到target_player场上，以sumtype召唤方式，sumpos表示形式]
     如果需要可选参数，则必须全部使用
    ●bool Duel.IsPlayerCanFlipSummon(int playerid, card pcard)
     bool Duel.IsPlayerCanFlipSummon(int player, Card c)
     检查玩家player是否可以反转召唤c
    ●bool Duel.IsPlayerCanSpecialSummonMonster(int playerid, int code, nil|int dat.setcode, nil|int dat.type, nil|int dat.attack, nil|int dat.defense, nil|int dat.level, nil|int dat.race, nil|int dat.attribute, [int pos, int toplayer, int sumtype])
     bool Duel.IsPlayerCanSpecialSummonMonster(int player, int code, int setcode, int type, int atk, int def, int level, int race, int attribute
     [, integer pos=POS_FACEUP, integer target_player=player, int sumtype])
     检查玩家player是否可以以pos的表示形式特殊召唤给定参数的怪兽到target_player场上
     此函数通常用于判定是否可以特招token和陷阱怪兽
    ●bool Duel.IsPlayerCanSpecialSummonCount(int playerid, int count)
     bool Duel.IsPlayerCanSpecialSummonCount(int player, int count)
     检查玩家player能否特殊召唤count次
    ●bool Duel.IsPlayerCanRelease(int playerid, card pcard)
     bool Duel.IsPlayerCanRelease(int player, Card c)
     检查玩家player是否能解放c
    ●bool Duel.IsPlayerCanRemove(int playerid, card pcard)
     bool Duel.IsPlayerCanRemove(int player, Card c)
     检查玩家player是否能除外c
    ●bool Duel.IsPlayerCanSendtoHand(int playerid, card pcard)
     bool Duel.IsPlayerCanSendtoHand(int player, Card c)
     检查玩家是否能把c送去手牌
    ●bool Duel.IsPlayerCanSendtoGrave(int playerid, card pcard)
     bool Duel.IsPlayerCanSendtoGrave(int player, Card c)
     检查玩家是否能把c送去墓地
    ●bool Duel.IsPlayerCanSendtoDeck(int playerid, card pcard)
     bool Duel.IsPlayerCanSendtoDeck(int player, Card c)
     检查玩家是否能把c送去卡组
    ●bool Duel.IsPlayerCanAdditionalSummon(int playerid)
    ●bool Duel.IsChainNegatable(int chaincount)
     bool Duel.IsChainNegatable(int chainc)
     检查连锁chainc的发动能否被无效
    ●bool Duel.IsChainDisablable(int chaincount)
     bool Duel.IsChainDisablable(int chainc)
     检查连锁chainc的效果能否被无效
    ●bool Duel.CheckChainTarget(int chaincount, card pcard)
     bool Duel.CheckChainTarget(int chainc, Card c)
     检查c是否是连锁chainc的效果的正确的对象
    ●bool Duel.CheckChainUniqueness()
     bool Duel.CheckChainUniqueness()
     检查当前连锁中是否存在同名卡的发动，true表示无同名卡
    ●int Duel.GetActivityCount(int playerid, int activity_type)
     int,... Duel.GetActivityCount(int player, int activity_type, ...)
     返回player进行对应的activity_type操作的次数
     activity_type为以下类型
     ACTIVITY_SUMMON         召唤（不包括通常召唤的放置）
     ACTIVITY_NORMALSUMMON   通常召唤（包括通常召唤的放置）
     ACTIVITY_SPSUMMON       特殊召唤
     ACTIVITY_FLIPSUMMON     反转召唤
     ACTIVITY_ATTACK         攻击
     ACTIVITY_BATTLE_PHASE   进入战斗阶段
    ●bool Duel.CheckPhaseActivity()
     bool Duel.CheckPhaseActivity()
     检查玩家在当前阶段是否有操作（是否处于阶段开始时，如七皇之剑）
    ●nil Duel.AddCustomActivityCounter(int counter_id, int activity_type, function counter_filter)
     void Duel.AddCustomActivityCounter(int counter_id, int activity_type, function f)
     设置操作类型为activity_type、代号为counter_id的计数器，放在initial_effect函数内
     f为过滤函数，以Card类型为参数，返回值为false的卡片进行以下类型的操作，计数器增加1（目前最多为1）
     activity_type为以下类型
     ACTIVITY_SUMMON         召唤（不包括通常召唤的set）
     ACTIVITY_NORMALSUMMON   通常召唤（包括通常召唤的set）
     ACTIVITY_SPSUMMON       特殊召唤
     ACTIVITY_FLIPSUMMON     反转召唤
     ACTIVITY_CHAIN          发动效果
    ●int Duel.GetCustomActivityCount(int counter_id, int playerid, int activity_type)
     int Duel.GetCustomActivityCount(int counter_id, int player, int activity_type)
     代号为counter_id的计数器的计数，返回player进行以下操作的次数（目前最多为1）
     activity_type为以下类型
     ACTIVITY_SUMMON         召唤（不包括通常召唤的set）
     ACTIVITY_NORMALSUMMON   通常召唤（包括通常召唤的set）
     ACTIVITY_SPSUMMON       特殊召唤
     ACTIVITY_FLIPSUMMON     反转召唤
     ACTIVITY_CHAIN          发动效果
    ●int Duel.GetBattledCount(int playerid)
     int Duel.GetBattledCount(int player)
     返回玩家player这回合战斗过的次数 
    ●bool Duel.IsAbleToEnterBP()
     bool Duel.IsAbleToEnterBP()
     检查回合玩家能否进入战斗阶段
    ●bool Duel.VenomSwampCheck(? ?, card pcard)
     bool Duel.VenomSwampCheck(Effect e, Card c)
     #蛇毒沼泽专用。把攻击力被其效果变成0的卡片破坏
    ●nil Duel.SwapDeckAndGrave(int playerid)
     void Duel.SwapDeckAndGrave(int player)
     现世与冥界的逆转专用。把玩家player的卡组和墓地交换
    ●nil Duel.MajesticCopy(card pcard, card ccard)
     void Duel.MajesticCopy(Card c1, Card c2)
     救世星龙专用。把c2记述的效果复制给c1
     强制发动的效果可以选择是否发动
     ##只说明常用的函数
    ●int Debug.Message()
     void Debug.Message(any msg)
     显示消息
    ●card Debug.AddCard(int code, int owner, int playerid, int location, int sequence, int position, [bool proc])
     Card Debug.AddCard(int code, int owner, int player, int location, int seq, int pos[, bool proc=false])
     添加卡片，将卡号为code的卡片的持有者设置为owner，以表示形式pos放置在player的场上位于location上序号为seq的格子处
     proc=true则解除苏生限制
    ●nil Debug.SetPlayerInfo(int playerid, int lp, int startcount, int drawcount)
     void Debug.SetPlayerInfo(int playerid, int lp, int startcount, int drawcount)
     设置玩家信息，基本分为lp，初始手卡为startcount张，每回合抽drawcount张
     playerid 下方 0,上方 1
    ●nil Debug.PreSummon(card pcard, int summon_type, [int summon_location])
     void Debug.PreSummon(Card c, int sum_type[, int sum_location=0])
     设置卡片c的召唤信息：以sum_type方法(通常召唤、特殊召唤等)[从sum_location]出场
    ●bool Debug.PreEquip(card equip_card, card target)
     bool Debug.PreEquip(Card equip_card, Card target)
     为target添加装备equip_card
    ●nil Debug.PreSetTarget(card t_card, card target)
     void Debug.PreSetTarget(Card c, Card target)
     把target选为c的永续对象
    ●nil Debug.PreAddCounter(card pcard, int countertype, [int count])
     void Debug.PreAddCounter(Card c, int counter_type, int count)
     为c添加count个counter_type的指示物
    ●nil Debug.ReloadFieldBegin(int flag, [int rule])
     void Debug.ReloadFieldBegin(int flag)
     以选项flag开始布局
        flag 残局：DUEL_ATTACK_FIRST_TURN+DUEL_SIMPLE_AI
    ●nil Debug.ReloadFieldEnd()
     void Debug.ReloadFieldEnd()
     布局结束
    ●nil Debug.SetAIName(string pstr)
     void Debug.SetAIName(string name)
     设置AI的名字
    ●nil Debug.ShowHint(string pstr)
     void Debug.ShowHint(string msg)
     显示消息提示框

    ●void initial_effect(Card c)
    载入卡片时调用
    一般是注册初始卡片效果，以及设置苏生限制等等
    ●int bit.band(int a, int b)
    a与b的位与
    ●int bit.lshift(int a, int b)
    a左移b
    ●int bit.bor(int a, int b)
    a与b的位或
    ●int bit.rshift(int a, int b)
    a右移b
    ●int bit.bxor(int a, int b)
    a与b的位异或
    ●int Card.GetDefense(Card c)
    返回c的当前守备力，返回值是负数表示是"?"
    ●void Card.SetTurnCounter(Card c, int counter)
    设置c的回合计数器（光之护封剑等）
    ●void Card.TrapMonsterComplete(Card c, int extra_type)
    使陷阱怪兽c占用一个魔法陷阱格子，并添加extra_type怪兽类型
    注：陷阱怪兽属性指的是同时作为怪兽和陷阱，并且额外使一个魔法陷阱的格子不能使用
    ●void Duel.ReplaceAttacker(Card c)
    #用c代替当前攻击的卡进行伤害阶段
    ●void Duel.ReplaceAttackTarget(Card c)
    (预留）
    ●int aux.Stringid(int code, int id)
    用于索引卡号为code的卡片第id个（从0开始）效果提示
    ●function aux.TargetEqualFunction(function f, value, a, b, c)
    return	function(effect,target)
                return f(target,a,b,c)==value
            end
    ●function aux.TargetBoolFunction(function f, a, b, c)
    return	function(effect,target)
                return f(target,a,b,c)
            end
    ●function aux.FilterEqualFunction(function f, value, a, b, c)
    return	function(target)
                return f(target,a,b,c)==value
            end
    ●function aux.FilterBoolFunction(function f, a, b, c)
    return	function(target)
                return f(target,a,b,c)
            end
    ●function aux.NonTuner(function f, a, b, c)
    return	function(target)
                return target:IsNotTuner() and (not f or f(target,a,b,c))
            end
    ●void aux.AddSynchroProcedure(Card c, function f1, function f2, int ct)
    为c添加同调召唤手续
    f1为调整满足的过滤条件，f2为调整以外满足的过滤条件（通常用aux.NonTuner）
    调整以外的怪兽至少需要ct只
    ●void aux.AddSynchroProcedure2(Card c, function f1, function f2)
    为c添加同调召唤手续
    f1为调整满足的过滤条件，f2为调整以外满足的过滤条件（通常用aux.NonTuner）
    只能用1只调整以外的怪兽
    ●void aux.AddXyzProcedure(Card c, function f, int lv, int ct[, function alterf|nil, int desc|nil, int maxct=ct, function op|nil])
    为c添加超量召唤手续
    用满足条件f的等级为lv的ct-maxct只怪兽进行叠放
    其余的参数用于在单个怪兽（通常是超量怪兽）上叠放
    alterf为这个怪兽满足的条件，desc为描述，op为叠放时需要的操作（希望皇龙）
    ●void aux.AddFusionProcCode2(Card c, int code1, int code2, bool sub, bool insf)
    为c指定卡号为code1和code2的怪兽为融合素材
    sub表示能否使用融合代替素材，insf表示能否用简易融合召唤
    ●void aux.AddFusionProcCode3(Card c, int code1, int code2, int code3, bool sub, bool insf)
    为c指定卡号为code1,code2,code3的怪兽为融合素材
    ●void aux.AddFusionProcCode4(Card c, int code1, int code2, int code3, int code4, bool sub, bool insf)
    为c指定卡号为code1,code2,code3,code4的怪兽为融合素材
    ●void aux.AddFusionProcCodeFun(Card c, int code, function f, int cc, bool sub, bool insf)
    为c指定卡号号为code和cc个满足条件f的怪兽为融合素材
    ●void aux.AddFusionProcFun2(Card c, function f1, function f2, bool insf)
    为c指定满足条件f1与f2的怪兽为融合素材
    ●void aux.AddFusionProcCodeRep(Card c, int code, int cc, bool sub, bool insf)
    为c指定cc个相同的怪兽为融合素材，code为卡号
    ●void aux.AddFusionProcFunRep(Card c, function f, int cc, bool insf)
    为c指定cc个满足相同条件f的怪兽为融合素材
    ●void aux.AddRitualProcGreater(Card c, function filter)
    为c添加仪式召唤效果
    filter为仪式怪兽满足的条件，素材的等级之和可以超过仪式怪兽的等级
    ●void aux.AddRitualProcEqual(Card c, function filter)
    为c添加仪式召唤效果
    filter为仪式怪兽满足的条件，素材的等级之和必须等于仪式怪兽的等级
    ●void aux.EnablePendulumAttribute(Card c[, active_effect=true])
    为灵摆怪兽c添加灵摆怪兽属性（灵摆召唤，灵摆卡的发动）
    active_effect=false则不注册灵摆卡“卡的发动”的效果
    ●void aux.EnableDualAttribute(Card c)
    为c添加二重怪兽属性
    ●bool aux.IsDualState(Effect e)
    检查二重怪兽e:GetHandler()是否是再度召唤状态（用于效果的Condition属性）
    常用于二重怪兽再度召唤获得的效果e的Condition属性
    ●bool aux.DualNormalCondition(Effect e)
    检查二重怪兽e:GetHandler()是否为被视为通常怪兽的状态（用于效果的Condition属性）
    ●bool aux.IsNotDualState(Effect e)
    aux.IsDualState的反义（用于效果的Condition属性）
    ●bool aux.IsUnionState(Effect e)
    检查同盟怪兽e:GetHandler()是否处于同盟装备的状态（用于效果的Condition属性）
    ●void aux.SetUnionState(Card c)
    为c添加同盟怪兽属性
    ●bool aux.CheckUnionEquip(Card uc, Card tc)
    检查同盟怪兽uc能否作为同盟装备在怪兽tc上
    ●void aux.EnableSpiritReturn(Card c, int event1,...)
    为c添加灵魂怪兽结束阶段回到手卡的效果（发生事件event1,...的回合，结束阶段回到手卡）
    ●function aux.NecroValleyFilter(function f)
    根据过滤条件f返回一个新的过滤条件：满足f并且不受王家长眠之谷的影响的卡
    ●void aux.BeginPuzzle()
    开始残局
    ##此函数注册3个全局效果：
    ##回合结束时玩家的基本分变成0
    ##跳过抽卡阶段与准备阶段
