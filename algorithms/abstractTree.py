from helpers import functions
import graphviz


class Node:
    def __init__(self, value, index, left=None, right=None):
        self.value = value
        self.index = index
        self.left = left
        self.right = right


def getTreeHeight(root):
    if not root:
        return 0
    return max(getTreeHeight(root.left) + 1, getTreeHeight(root.right) + 1)


def getNumberOfNodes(root):
    if not root:
        return 0
    return getNumberOfNodes(root.left) + getNumberOfNodes(root.right) + 1


def getSetOfVarProps(root):
    if not root:
        return set()
    if not 'a' <= root.value <= 'z':
        return set(getSetOfVarProps(root.left).union(getSetOfVarProps(root.right)))
    return set(getSetOfVarProps(root.left).union(getSetOfVarProps(root.right)).union(set(root.value)))


def tree(i, j, formula, islp, ruleType, split, nodeIndex):
    if not islp[i][j]:
        return
    if ruleType[i][j] == functions.Rule.baseRule:
        result = Node(formula[i], nodeIndex)
        return result, nodeIndex
    if ruleType[i][j] == functions.Rule.andRule:
        result = Node('&', nodeIndex)
        result.left, a = tree(i + 1, split[i][j] - 1, formula, islp, ruleType, split, nodeIndex + 1)
        result.right, b = tree(split[i][j] + 1, j - 1, formula, islp, ruleType, split, a + 1)
        return result, b
    if ruleType[i][j] == functions.Rule.orRule:
        result = Node('|', nodeIndex)
        result.left, a = tree(i + 1, split[i][j] - 1, formula, islp, ruleType, split, nodeIndex + 1)
        result.right, b = tree(split[i][j] + 1, j - 1, formula, islp, ruleType, split, a + 1)
        return result, b
    if ruleType[i][j] == functions.Rule.notRule:
        result = Node('~', nodeIndex)
        result.left, a = tree(i + 1, j, formula, islp, ruleType, split, nodeIndex + 1)
        return result, a


def makeTreeGraph(binaryTree, graph):
    graph.node(str(binaryTree.index), binaryTree.value)
    if binaryTree.left:
        graph.edge(str(binaryTree.index), str(binaryTree.left.index))
        makeTreeGraph(binaryTree.left, graph)
    if binaryTree.right:
        graph.edge(str(binaryTree.index), str(binaryTree.right.index))
        makeTreeGraph(binaryTree.right, graph)


def createTree(formula, output):
    if len(formula) == 0:
        return
    invalidIndex, valid = functions.validate(formula)
    functions.printIfValid(valid, invalidIndex, output, formula)
    islp, ruleType, split = functions.parse(formula)
    if islp[0][len(formula) - 1]:
        binaryTree, _ = tree(0, len(formula) - 1, formula, islp, ruleType, split, 0)
        graph = graphviz.Digraph(format='png')
        makeTreeGraph(binaryTree, graph)
        graph.render(f'graphs/graph')
        return True, getTreeHeight(binaryTree), getNumberOfNodes(binaryTree), getSetOfVarProps(binaryTree)
    else:
        functions.insertInTextbox(output, f"Formula {formula} nu face parte din LP.")
        return False
