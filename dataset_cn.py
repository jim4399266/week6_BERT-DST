import json
import numpy as np

class Turn_cn:
    # 修改此类，对应数据集格式
    def __init__(self, transcript, turn_label, system_transcript, asr=None, num=None):
        self.transcript = transcript
        self.turn_label = turn_label
        self.system_transcript = system_transcript
        self.asr = asr or []
        self.num = num or {}

    def to_dict(self):
        return {
                'transcript': self.transcript,
                'turn_label': self.turn_label,
                'system_transcript': self.system_transcript,
                'num': self.num}

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

class Dialogue_cn:
    def __init__(self, turns):
        # 英文数据集中，一个turn由sys_transcript和transcript组成，且sys文本在前
        # 中文数据集中，一个turn只有一句文本，要么是sys的，要么是usr的，且usr文本在前
        self.__integrate_turn(turns)

    def __integrate_turn(self, turns):
        self.turns = []
        for idx in range(0, len(turns), 2):
            item1 = turns[idx]
            try:
                item2 = turns[idx+1]
            except:
                # 若超出范围，添加一个空item
                item2 = {
                    'utterance': None,
                    "dialog_act": [],
                }
            transcript = item1['utterance']
            system_transcript = item2['utterance']
            turn_label = []
            for dialog_act in item1["dialog_act"] + item2["dialog_act"]:
                # 添加 slot-value 对
                if (dialog_act[-2] not in ['', ' ', 'none', None] and dialog_act[-1] not in ['', ' ', 'none', None]) :
                    turn_label.append([dialog_act[-2], dialog_act[-1]])
            t = {
                'transcript': transcript,
                'system_transcript': system_transcript,
                'turn_label': turn_label
            }
            # 创建Turn_cn的对象
            self.turns.append(Turn_cn.from_dict(t))

    def __len__(self):
        return len(self.turns)

    def to_dict(self):
        return {'turns': [t.to_dict() for t in self.turns]}

    @classmethod
    def from_dict(cls, d):
        # 由于中文数据集和英文数据集在turn上结构不同，修改此处代码
        return cls([t for t in d['turns']])
        # return cls([Turn_cn.from_dict(t) for t in d['turns']])

class Dataset_cn:
    def __init__(self, dialogues):
        self.dialogues = dialogues

    def __len__(self):
        return len(self.dialogues)

    def iter_turns(self):
        for d in self.dialogues:
            for t in d.turns:
                yield t

    def to_dict(self):
        return {'dialogues': [d.to_dict() for d in self.dialogues]}

    @classmethod
    def from_dict(cls, d):
        return cls([Dialogue_cn.from_dict(dd) for dd in d])

    def evaluate_preds_cn(self, preds):
        request = []
        inform = []
        joint_goal = []
        fix = {'centre': 'center', 'areas': 'area', 'phone number': 'number'}
        i = 0
        for d in self.dialogues:
            pred_state = {}
            for t in d.turns:
                gold_request = set([(s, v) for s, v in t.turn_label if s == 'request'])
                gold_inform = set([(s, v) for s, v in t.turn_label if s != 'request'])
                pred_request = set([(s, v) for s, v in preds[i] if s == 'request'])
                pred_inform = set([(s, v) for s, v in preds[i] if s != 'request'])
                request.append(gold_request == pred_request)
                inform.append(gold_inform == pred_inform)

                gold_recovered = set()
                pred_recovered = set()
                for s, v in pred_inform:
                    pred_state[s] = v
                for b in t.belief_state:
                    for s, v in b['slots']:
                        if b['act'] != 'request':
                            gold_recovered.add((b['act'], fix.get(s.strip(), s.strip()), fix.get(v.strip(), v.strip())))
                for s, v in pred_state.items():
                    pred_recovered.add(('inform', s, v))
                joint_goal.append(gold_recovered == pred_recovered)
                i += 1
        return {'turn_inform': np.mean(inform), 'turn_request': np.mean(request), 'joint_goal': np.mean(joint_goal)}

class Ontology_cn:
    def __init__(self, slots=None, values=None, num=None):
        self.slots = slots or []
        self.values = values or {}
        self.num = num or {}

    def to_dict(self):
        return {'slots': self.slots, 'values': self.values, 'num': self.num}

    @classmethod
    def from_dict(cls, d):
        return cls(**d)
