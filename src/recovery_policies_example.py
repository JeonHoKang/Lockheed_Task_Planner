from alter_tree import AlterTree

toolset = AlterTree()
contingency = toolset.contingency_name

def recover_screw_stuck():
    planning_node = AlterTree().contingency_plan['id']
    toolset.add_node(planning_node, "screw_stuck", "sequential")
    toolset.add_node("screw_stuck", "recovery-unscerw", "independent", 'r3', 6, 0)
    toolset.add_node("screw_stuck", "recovery-rescrew", "independent", 'r3', 8, 1)

# def dropped_part():


def main():
    recover_screw_stuck()
    print('done')

if __name__ == "__main__":
    main()
