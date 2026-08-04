from anymal_model import load_anymal_reduced

model = load_anymal_reduced()
for jid in range(1, model.njoints):
    j = model.joints[jid]
    print("j looks like : \n",j)
    # print(f"{jid:2d} {model.names[jid]:<12s} {j.shortname():<24s} "
    #       f"q[{j.idx_q}:{j.idx_q + j.nq}]  v[{j.idx_v}:{j.idx_v + j.nv}]")

