# metrics_demo.py
# 评测指标演示：从混淆矩阵的四个格，算出准确率、精确率、召回率、F1


def calc_metrics(tp, fp, tn, fn):
    """输入混淆矩阵四格，打印四个评测指标。

    tp: 真通过（判 Pass，实际该 Pass）
    fp: 误放（判 Pass，实际该 Fail）—— 放过坏结果，危险
    tn: 真失败（判 Fail，实际该 Fail）
    fn: 误杀（判 Fail，实际该 Pass）—— 冤枉好结果
    """
    total = tp + fp + tn + fn

    # 准确率：判对的占比
    if total == 0:
        accuracy = 0
    else:
        accuracy = (tp + tn) / total

    # 精确率：我判 Pass 的里面，有多少是真对
    if tp + fp == 0:
        precision = 0
    else:
        precision = tp / (tp + fp)

    # 召回率：所有真对的里面，我抓到了多少
    if tp + fn == 0:
        recall = 0
    else:
        recall = tp / (tp + fn)

    # F1：精确率和召回率的调和平均
    if precision + recall == 0:
        f1 = 0
    else:
        f1 = 2 * precision * recall / (precision + recall)

    print("========== 评测指标 ==========")
    print("准确率 Accuracy ：", round(accuracy * 100, 2), "%")
    print("精确率 Precision：", round(precision * 100, 2), "%")
    print("召回率 Recall   ：", round(recall * 100, 2), "%")
    print("F1 值           ：", round(f1 * 100, 2), "%")
    print("==============================")


# 验证：模拟评测 100 条用例
# TP=80  FP=2（误放）  TN=15  FN=3（误杀，含 TC-TRACE-001 那种情况）
# 手算预期：准确率95%  精确率97.56%  召回率96.39%  F1 96.97%
print("模拟场景：评测 100 条用例")
calc_metrics(tp=80, fp=2, tn=15, fn=3)

# 边界验证：分母全为 0，不能崩
print("\n边界场景：四个数全为 0")
calc_metrics(tp=0, fp=0, tn=0, fn=0)
