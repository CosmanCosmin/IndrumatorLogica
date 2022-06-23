from helpers import functions

count = 0


def printInductiveCases(i, j, formula, islp, ruleType, split, output):
    global count
    if 0 <= i <= j < len(formula):
        if islp[i][j]:
            if ruleType[i][j] == functions.Rule.baseRule:
                functions.insertInTextbox(output,
                                          f"Formula {count + 1} = {formula[i:j + 1]}"
                                          f" face parte din LP [aplicând pasul de bază]\n")
                count += 1
                return count
            if ruleType[i][j] == functions.Rule.notRule:
                if formula[i] == '~':
                    if j > i:
                        val = printInductiveCases(i + 1, j, formula, islp, ruleType, split, output)
                        functions.insertInTextbox(output,
                                                  f"Formula {count + 1} = {formula[i:j + 1]} face parte din LP"
                                                  f" [aplicând pasul inductiv unu pe Formula {val} ="
                                                  f" {formula[i + 1:j + 1]}]\n")
                        count += 1
                        return count
            if ruleType[i][j] == functions.Rule.orRule:
                if (formula[i] == '(' and formula[j] == ')') and j > i:
                    if (split[i][j] - 1 >= i + 1 and split[i][j] + 1 <= j - 1) and formula[split[i][j]] == '|':
                        val1 = printInductiveCases(i + 1, split[i][j] - 1, formula, islp, ruleType, split, output)
                        val2 = printInductiveCases(split[i][j] + 1, j - 1, formula, islp, ruleType, split, output)
                        functions.insertInTextbox(output,
                                                  f"Formula {count + 1} = {formula[i:j + 1]} face parte din LP"
                                                  f" [aplicând pasul inductiv doi pe Formula {val1} ="
                                                  f" {formula[i + 1:split[i][j]]}"
                                                  f" și pe Formula {val2} = {formula[split[i][j] + 1:j]}]\n")
                        count += 1
                        return count
            if ruleType[i][j] == functions.Rule.andRule:
                if (formula[i] == '(' and formula[j] == ')') and j > i:
                    if (split[i][j] - 1 >= i + 1 and split[i][j] + 1 <= j - 1) and formula[split[i][j]] == '&':
                        val1 = printInductiveCases(i + 1, split[i][j] - 1, formula, islp, ruleType, split, output)
                        val2 = printInductiveCases(split[i][j] + 1, j - 1, formula, islp, ruleType, split, output)
                        functions.insertInTextbox(output,
                                                  f"Formula {count + 1} = {formula[i:j + 1]} face parte din LP"
                                                  f" [aplicând pasul inductiv trei pe Formula {val1} ="
                                                  f" {formula[i + 1:split[i][j]]}"
                                                  f" și pe Formula {val2} = {formula[split[i][j] + 1:j]}]\n")
                        count += 1
                        return count


def giveResults(formula, islp, ruleType, split, output):
    if islp[0][len(formula) - 1]:
        printInductiveCases(0, len(formula) - 1, formula, islp, ruleType, split, output)
        functions.insertInTextbox(output, f"Astfel, formula {formula} face parte din LP.\n")
    else:
        functions.insertInTextbox(output, f"Formula {formula} nu face parte din LP.")
    global count
    count = 0


def checkIfLP(formula, output):
    if len(formula) == 0:
        return
    functions.insertInTextbox(output, formula + '\n')
    invalidIndex, valid = functions.validate(formula)
    functions.printIfValid(valid, invalidIndex, output, formula)
    islp, ruleType, split = functions.parse(formula)
    giveResults(formula, islp, ruleType, split, output)
