import fuzzy.storage.fcl.Reader
import random
import output as op


global main_text
global rule_block
global input_template
global fuzzify_template
global output_template
global defuzzify_template
global improvment

input_vars = {'2':'betweeness_centrality','3':'load_centrality',
    '4':'out_degree','5':'in_degree','6':'closeness_centrality'}
output_vars = {'1':'god_class','2':'lazy_class','3':'feature_envy','4':'shotgun_surgery'}
terms = {'1': 'very_low', '2': 'low', '3': 'middle', '4': 'high', '5':'very_high'}
operators = {'1':'OR', '2':'AND'}

main_text = 'FUNCTION_BLOCK automated_refactoring\n'

rule_block = ''

input_template = "\tVAR_INPUT\n\
        \tbetweeness_centrality : REAL; (* min=0.0,max={0}*)\n\
        \tload_centrality : REAL; (* min=0.0,max={1}*)\n\
        \tout_degree : REAL; (* min=0.0,max={2}*)\n\
        \tin_degree : REAL; (* min=0.0,max={3}*)\n\
        \tcloseness_centrality : REAL; (* min=0.0,max={4}*)\n\
    END_VAR\n"

fuzzify_template = "\tFUZZIFY {0}\n\
        \tTERM very_high := {1};\n\
        \tTERM high := {2};\n\
        \tTERM middle := {3};\n\
        \tTERM low := {4};\n\
        \tTERM very_low := {5};\n\
    END_FUZZIFY\n"

output_template = '\tVAR_OUTPUT\n\
        \tgod_class : REAL; (* min=0,max=1 *)\n\
        \tlazy_class : REAL; (* min=0,max=1 *)\n\
        \tfeature_envy : REAL; (* min=0,max=1 *)\n\
        \tshotgun_surgery : REAL; (* min=0,max=1 *)\n\
    END_VAR\n'

defuzzify_template = '\tDEFUZZIFY god_class\n\
        \tTERM very_high := (0.75,0) (1,1);\n\
        \tTERM high := (0.5,0)(0.75,1)(1,0);\n\
        \tTERM middle := (0.25,0)(0.5,1)(0.75,0);\n\
        \tTERM low := (0,0)(0.25,1)(0.5,0);\n\
        \tTERM very_low := (0,1) (0.25,0);\n\
        \tACCU : MAX; (* AlgebraicSum *)\n\
        \tMETHOD : COG;\n\
        \tDEFAULT := 0;\n\
    END_DEFUZZIFY\n\
    \
    DEFUZZIFY lazy_class\n\
        TERM very_high := (0.75,0) (1,1);\n\
        TERM high := (0.5,0)(0.75,1)(1,0);\n\
        TERM middle := (0.25,0)(0.5,1)(0.75,0);\n\
        TERM low := (0,0)(0.25,1)(0.5,0);\n\
        TERM very_low := (0,1) (0.25,0);\n\
        ACCU : MAX; (* AlgebraicSum *)\n\
        METHOD : COG;\n\
        DEFAULT := 0;\n\
    END_DEFUZZIFY\n\
    \
    DEFUZZIFY feature_envy\n\
        \tTERM very_high := (0.75,0) (1,1);\n\
        \tTERM high := (0.5,0)(0.75,1)(1,0);\n\
        \tTERM middle := (0.25,0)(0.5,1)(0.75,0);\n\
        \tTERM low := (0,0)(0.25,1)(0.5,0);\n\
        \tTERM very_low := (0,1) (0.25,0);\n\
        \tACCU : MAX; (* AlgebraicSum *)\n\
        \tMETHOD : COG;\n\
        \tDEFAULT := 0;\n\
    END_DEFUZZIFY\n\
    \
    DEFUZZIFY shotgun_surgery\n\
        \tTERM very_high := (0.75,0) (1,1);\n\
        \tTERM high := (0.5,0)(0.75,1)(1,0);\n\
        \tTERM middle := (0.25,0)(0.5,1)(0.75,0);\n\
        \tTERM low := (0,0)(0.25,1)(0.5,0);\n\
        \tTERM very_low := (0,1) (0.25,0);\n\
        \tACCU : MAX; (* AlgebraicSum *)\n\
        \tMETHOD : COG;\n\
        \tDEFAULT := 0;\n\
    END_DEFUZZIFY\n'

rules_template = '\t\tRULE {0} (* stop *):\n \tIF \t{1} {2} {3} \tTHEN {4};'


def reverse_defuzzify(value):
    if value >= 0 and value < 0.25:
        return 'very_low'
    if value >= 0.25 and value < 0.5:
        return 'low'
    if value >= 0.5 and value < 0.75:
        return 'middle'
    if value >= 0.75 and value < 1:
        return 'high'
    if value == 1:
        return 'very_high'


def generate_fuzzification(fuzzify_valus):
    global main_text
    main_text = main_text + input_template.format(fuzzify_valus['betweeness_centrality']['max'],
        fuzzify_valus['load_centrality']['max'], fuzzify_valus['out_degree']['max'],
        fuzzify_valus['in_degree']['max'], fuzzify_valus['closeness_centrality']['max'])
    main_text += '\n' + output_template + '\n'

    for key, value in fuzzify_valus.items():
        main_text += '\n'
        step = value['max']/4.0
        v_low = '(0,1)(%s,0)'%step
        low = '(0,0)(%s,1)(%s,0)'%(step,step*2)
        middle = '(%s,0)(%s,1)(%s,0)'%(step,step*2,step*3)
        high = '(%s,0)(%s,1)(%s,0)'%(step*2,step*3,str(value['max']))
        v_high = '(%s,0)(%s,1)'%(step*3,str(value['max']))

        main_text += fuzzify_template.format(key, v_high, high,
            middle, low, v_low)


    main_text += '\n' + defuzzify_template + '\n'


def fitness(first=False):
    analyse_file = open('output.txt', 'r')
    analyse_text = analyse_file.read()
    classes = analyse_text.split('\n')
    analyse_json = {}
    in_degree = []
    out_degree = []
    betweeness = []
    load = []
    closeness = []
    fuzzify_valus = {}
    for clas in classes[1:]:
        parametrs = clas.split(' ')
        if len(parametrs) < 2:
            # print "empty line"
            continue
        analyse_json[parametrs[0]] = {}
        analyse_json[parametrs[0]]['in_degree'] = float(parametrs[4])
        in_degree.append(float(parametrs[4]))
        analyse_json[parametrs[0]]['out_degree'] = float(parametrs[5])
        out_degree.append(float(parametrs[5]))
        analyse_json[parametrs[0]]['betweeness'] = float(parametrs[6])
        betweeness.append(float(parametrs[6]))
        analyse_json[parametrs[0]]['load'] = float(parametrs[7])
        load.append(float(parametrs[7]))
        analyse_json[parametrs[0]]['closeness'] = float(parametrs[8])
        closeness.append(float(parametrs[8]))

    if first:
        fuzzify_valus['in_degree'] = {'min':min(in_degree),'max':max(in_degree)}
        fuzzify_valus['out_degree'] = {'min':min(out_degree),'max':max(out_degree)}
        fuzzify_valus['betweeness_centrality'] = {'min':min(betweeness),'max':max(betweeness)}
        fuzzify_valus['load_centrality'] = {'min':min(load),'max':max(load)}
        fuzzify_valus['closeness_centrality'] = {'min':min(closeness),'max':max(closeness)}

        generate_fuzzification(fuzzify_valus)

    in_degree_average = sum(in_degree)/float(len(in_degree))
    out_degree_average = sum(out_degree)/float(len(out_degree))
    betweeness_average = sum(betweeness)/float(len(betweeness))
    load_average = sum(load)/float(len(load))
    closeness_average = sum(closeness)/float(len(closeness))

    refactor_list = []

    for id, param in analyse_json.iteritems():
        critical_params = {}
        # critical_params[id] = {}
        if param['in_degree'] > in_degree_average:
            if id not in critical_params.keys():
                critical_params[id] = {}
            critical_params[id]['in_degree'] = param['in_degree']
        if param['out_degree'] > out_degree_average:
            if id not in critical_params.keys():
                critical_params[id] = {}
            critical_params[id]['out_degree'] = param['out_degree']
        if param['betweeness'] > betweeness_average:
            if id not in critical_params.keys():
                critical_params[id] = {}
            critical_params[id]['betweeness_centrality'] = param['betweeness']
        if param['load'] > load_average:
            if id not in critical_params.keys():
                critical_params[id] = {}
            critical_params[id]['load_centrality'] = param['load']
        if param['closeness'] > closeness_average:
            if id not in critical_params.keys():
                critical_params[id] = {}
            critical_params[id]['closeness_centrality'] = param['closeness']
        if len(critical_params.keys()) > 0:
            refactor_list.append(critical_params)
    analyse_file.close()

    return refactor_list

improvment = False

def generate_fuzzy(rules):
    global rule_block
    rule_block = ''
    rule_block += '\tRULEBLOCK automated_refactoring\n\
        \tAND : AlgebraicProduct;\
        \tOR : MAX;'
    index = 1
    for rule in rules:
        opr1 = input_vars[rule[1]] + ' IS ' + terms[rule[0]]
        opt = operators[rule[2]]
        opr2 = input_vars[rule[4]] + ' IS ' + terms[rule[3]]
        result = output_vars[rule[7]] + ' IS ' + terms[rule[6]]
        tmp = rules_template.format(str(index),opr1,opt,opr2,result)
        rule_block += '\n' + tmp + '\n'
        index += 1
    rule_block += '\tEND_RULEBLOCK\n\
END_FUNCTION_BLOCK\n\
        (*\
                INF = AlgebraicProduct()\n\
                ACC = AlgebraicSum()\n\
                COM = AlgebraicSum()\n\
                CER = AlgebraicProduct()\n\
                COG = fuzzy.defuzzify.COG.COG(INF=INF,ACC=ACC,failsafe = 0)\
        *)'
    fcl_file = open('rules.fcl', 'w+')
    fcl_file.write(main_text+'\n'+rule_block)
    fcl_file.close()


def fuzzy_genetic(class_id, params):
    global improvment
    dual_operand = []
    result_file = open('result.txt', 'a+')
    not_refactor = open('not_refactor.txt', 'a+')
    input_keys = input_vars.keys()

    for inp1 in range(len(input_vars.items())):
        for inp2 in range(inp1+1, len(input_vars.items())):
            for term in terms.iteritems():
                for oprt in operators.iteritems():
                    out = random.choice(output_vars.keys())
                    new_rule = term[0]+input_keys[inp1]+oprt[0]+term[0]+input_keys[inp2]+'0'+term[0]+out
                    dual_operand.append(new_rule)
    to_be_del = None
    while True:
        if len(dual_operand) <= 10:
            not_refactor.write(class_id + '\n')
            return
        for rule in dual_operand:
            try:
                if to_be_del is not None:
                    
                    ref_code = output_vars.keys()[output_vars.values().index(to_be_del)]
                    if ref_code == rule.split('0')[-1][-1]:
                        dual_operand.remove(rule)
            except Exception as e:
                print 'delete error', e
                continue
        parents = random.sample(dual_operand, int(0.8*len(dual_operand)))
        for idx in range(len(parents)/2):
            p1 = parents[idx].split('0')
            p2 = parents[idx+len(parents)/2].split('0')
            child1 = p1[0] +'0'+ p2[1]
            child2 = p2[0] +'0'+ p1[1]
            dual_operand.remove(parents[idx])
            dual_operand.remove(parents[idx+len(parents)/2])
            random_child = random.choice(range(0,2))
            if random_child == 0:
                tmp = list(child1)
                tmp[2] = '1' if tmp[2]=='2' else '2'
                child1 = ''.join(tmp)
            else:
                tmp = list(child2)
                tmp[2] = '1' if tmp[2]=='2' else '2'
                child2 = ''.join(tmp)
            dual_operand.append(child1)
            dual_operand.append(child2)
        generate_fuzzy(dual_operand)
        output0 = {'feature_envy':0.0,
            'shotgun_surgery':0.0,
            'god_class':0.0,
            'lazy_class':0.0
            }
        input1 = params
        system = fuzzy.storage.fcl.Reader.Reader().load_from_file("rules.fcl")
        system.calculate(input1, output0)
        critical_situation = False
        sec_critical_situation = False
        
        i = 0
        while i < len(output0.keys()):
            

            refactoring = output0.keys()[i]
            if not critical_situation:
                value = output0[refactoring]
            else:
                sec_critical_situation = True
            
            if value > 0:
                print('calculatin refactoring result', class_id, refactoring, reverse_defuzzify(value))
                op.generate(refactoring, class_id, reverse_defuzzify(value), improvment)
                new_params = fitness(False)

                deleted_rules = []
                class_fixed = True
                useless_refactoring = False
                for class_obj in new_params:
                    if class_obj.get(class_id) != None:
                        params = class_obj.get(class_id)
                        class_fixed = False

                if class_fixed :
                    result_file.write(str(class_id)+'  '+refactoring+'  '+reverse_defuzzify(value)+'\n')
                    return

                improvment = False
                checked = False
                for class_obj in new_params:
                    for bad_s, val in class_obj.get(class_id,{}).items():

                        if bad_s in params.keys():
                            if val > params[bad_s]:
                                critical_situation = False
                                sec_critical_situation = False
                                in_code = input_vars.keys()[input_vars.values().index(bad_s)]
                                deleted_rules.append(in_code)
                            elif val < params[bad_s]:
                                improvment = True
                                critical_situation = False
                                sec_critical_situation = False
                            elif val == params[bad_s]:
                                if not checked:
                                    checked = True
                                    if critical_situation and sec_critical_situation and value == 1:
                                        to_be_del = output0.keys()[i]
                                        critical_situation = False
                                        sec_critical_situation = False
                                    elif sec_critical_situation:
                                        value = 1
                                        i = i - 1
                                    else:
                                        critical_situation = True
                                        value = 0.01
                                        i = i - 1
                        else:
                            in_code = input_vars.keys()[input_vars.values().index(bad_s)]
                            deleted_rules.append(in_code)

                for rule in dual_operand:
                    try:
                        if to_be_del is not None:
                            
                            ref_code = output_vars.keys()[output_vars.values().index(to_be_del)]
                            if ref_code == rule.split('0')[-1][-1]:
                                dual_operand.remove(rule)
                        
                        for var in deleted_rules:
                            if var in rule.split('0')[0]:
                                dual_operand.remove(rule)
                    except Exception as e:
                        pass
            i = i + 1


def main():
    op.generate('start','', '', False)
    initial_values = fitness(first=True)
    bull = False
    for value in initial_values[2:]:
        
        for class_id, params in value.items():
            print 'class number ', class_id

            fuzzy_genetic(class_id, params)
            

main()
