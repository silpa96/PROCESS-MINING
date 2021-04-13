import os
import numpy as np
from dfg_to_petri import Custom
os.environ["PATH"] += os.pathsep + 'D:/Program Files (x86)/Graphviz2.38/bin/'
from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.algo.discovery.dfg import factory as dfg_factory
from pm4py.algo.discovery.inductive import factory as inductive_miner
from collections import Counter 
import math






def prob_dist(pos,p_values):
    N=sum(p_values)
    return p_values[pos]/N

def Ha(s,p_values):
    ent=0
    for i in range(s):
        t1=prob_dist(i,p_values)/prob_dist(s,p_values)
        t2=prob_dist(i,p_values)/prob_dist(s,p_values)
        en1=t1*math.log(t2)
        ent+=en1
    return -ent    

def Hb(s,p_values):
    ent=0
    for i in range(s,len(p_values)):
        t1=prob_dist(i,p_values)/(1-prob_dist(s,p_values))
        t2=prob_dist(i,p_values)/(1-prob_dist(s,p_values))
        en1=t1*math.log(t2)
        ent+=en1
    return -ent   

def delayed_insert(label,index,message):
    label.insert(index,message)  

def max_entropy(p_values):
    ents=[]
    for i in range(len(p_values)):
        ent=Ha(i,p_values)+Hb(i,p_values)
        ents.append(ent)
    ents=np.array(ents)
    s=np.argmax(ents)
    return s







def load_process(path,lb1):
    t=100
    lp=0
    lb1.after(t,delayed_insert,lb1,lp,'Loading log file')
    t+=100
    lp+=1
    global log
    log = xes_importer.import_log(path)
    
    d=Counter({('A','B'):3, ('A','B'):5, ('B','C'):2}) 
    from pm4py.visualization.dfg import factory as dfg_vis_factory
    dfg = dfg_factory.apply(log)
    gviz = dfg_vis_factory.apply(dfg, log=log, variant="frequency")
    dfg_vis_factory.view(gviz)

    lb1.after(t,delayed_insert,lb1,lp,'Converting to DFG')
    t+=100
    lp+=1
    # print(dfg)

    # frequency matrix
    lb1.after(t,delayed_insert,lb1,lp,'Extracting edges')
    t+=100
    lp+=1
    edges=list(dfg.keys())
    lb1.after(t,delayed_insert,lb1,lp,'Extracting events')
    t+=100
    lp+=1
    events=[]
    for i,j in edges:
        events.append(i)
        events.append(j)
    events=list(set(events))
    lb1.after(t,delayed_insert,lb1,lp,'Sorting events')
    t+=100
    lp+=1
    print(events)
    events.sort()
    print(events)
    lb1.after(t,delayed_insert,lb1,lp,'Calculating freaquencies')
    t+=100
    lp+=1
    fmatrix=[]
    for i in events:
        f1=[]
        for j in events:
            f1.append(dfg[i,j])
        fmatrix.append(f1)
    print(fmatrix)        
   
    lb1.after(t,delayed_insert,lb1,lp,'Frequency matrix created')
    t+=100
    lp+=1
    f_matrix=fmatrix

    #frequency threshold
    import math
    lb1.after(t,delayed_insert,lb1,lp,'Calulating frequency threshold')
    t+=100
    lp+=1
    n_traces=len(log)
    n_events=len(events)
    un_rate=0.03
    val1=(n_traces/n_events)*un_rate
    f_thres=1+round(val1)
    lb1.after(t,delayed_insert,lb1,lp,str(f_thres))
    t+=100
    lp+=1

    print(n_traces)
    print(n_events)
    print(f_thres)


#improved matrix
    lb1.after(t,delayed_insert,lb1,lp,'Calculating total frequency')
    t+=100
    lp+=1
    f_total=0
    for i in range(len(events)):
        for j in range(len(events)):
            f_total+=f_matrix[i][j]
    print(f_total)
    lb1.after(t,delayed_insert,lb1,lp,'Calculating total non zero frequency')
    t+=100
    lp+=1
    f_count=0
    for i in range(len(events)):
        for j in range(len(events)):
            if f_matrix[i][j]!=0:
                f_count+=1
    print(f_count)



#
    lb1.after(t,delayed_insert,lb1,lp,'Calculating parellel structure decision threshold')
    t+=100
    lp+=1

    p_thresh=f_total/f_count
    print(p_thresh)
    p_matrix=fmatrix
    for i in range(len(events)):
        for j in range(len(events)):
            f1=fmatrix[i][j] 
            if f1<f_thres:
                p_matrix[i][j]=0
                continue
            if i==j:
                continue
            f1=fmatrix[i][j] 
            f2=fmatrix[j][i]
            if f1>f_thres and f2>f_thres:
                fsum=f1+f2
                if fsum>p_thresh:
                    fprod=f1*f2
                    if fprod!=0:
                        p_matrix[i][j]=0
        
                            #f_matrix)
                               
    improved_matrix=p_matrix
    print(p_matrix)
    lb1.after(t,delayed_insert,lb1,lp,'Improved matrix created')
    t+=100
    lp+=1





    #
    import ppscore as pps
    import pandas as pd
    
    lb1.after(t,delayed_insert,lb1,lp,'Calculating predictive powerscore')
    t+=100
    lp+=1
    p_matrix1=np.corrcoef(np.array(p_matrix))
    p_matrix1[p_matrix1<0] = 0

    lb1.after(t,delayed_insert,lb1,lp,'Conversion to dataframe')
    t+=100
    lp+=1
    df=pd.DataFrame()
    c=0
    for i in range(n_events):
    
        col=[]
        for j in range(n_events):
            col.append(p_matrix[j][i])
        key='k'+str(c)
        df[key]=col
        c+=1

    print(df.head())
    pr_df=pps.matrix(df).pivot(columns='x', index='y',  values='ppscore')
  

    pr_matrix=p_matrix

    c=0
    lb1.after(t,delayed_insert,lb1,lp,'Getiing pps values')
    t+=100
    lp+=1
    for i in range(n_events):
        key='k'+str(c)
        df1=list(pr_df[key].tolist())
        for j in range(n_events):
            pr_matrix[i][j]=df1[j]
        c+=1    
    print(pr_matrix) 

    lb1.after(t,delayed_insert,lb1,lp,'Conversion back to matrix')
    t+=100  
    lp+=1 
    
    lb1.after(t,delayed_insert,lb1,lp,'Getiing list of pps')
    t+=100
    lp+=1
    p_values=[]

    for i in range(n_events):
        for j in range(n_events):
            if p_matrix1[i][j]>0:
                p_values.append(p_matrix1[i][j])
    lb1.after(t,delayed_insert,lb1,lp,'Sorting the list')
    t+=100
    lp+=1
    p_value=p_values.sort()
    print(p_values)


    lb1.after(t,delayed_insert,lb1,lp,'Getting Probability distributions')
    t+=100
    lp+=1
    lb1.after(t,delayed_insert,lb1,lp,'Calculating entropies')
    t+=100
    lp+=1
    lb1.after(t,delayed_insert,lb1,lp,'Applying maximum entropy principle')
    t+=100
    lp+=1
    lb1.after(t,delayed_insert,lb1,lp,'Calculating correlation thrshold')
    t+=100
    lp+=1
    s= max_entropy(p_values)
    print(s)
    corr_threshold=p_values[s]
    print('===========================================')
    print(corr_threshold)
    print(p_matrix1)
    print('============================================')

    c=0
    matrix_for_dfg=improved_matrix
    lb1.after(t,delayed_insert,lb1,lp,'Building DFG')
    t+=100
    lp+=1
    for i in range(n_events):
        for j in range(n_events):
            if p_matrix1[i][j]<corr_threshold and improved_matrix[i][j]<f_thres and i==j:
              
                matrix_for_dfg[i][j]=0
            else:
                c+=1

    print(c)
    i_count=0
    for i in range(len(events)):
        for j in range(len(events)):
            if matrix_for_dfg[i][j]!=0:
                i_count+=1
    print(i_count)
        d={} 





    lb1.after(t,delayed_insert,lb1,lp,'Detecting selective structures')
    t+=100
    lp+=1


    print('Detecting selective structures')
    selective=[]
    for i in range(len(events)):
        for j in range(len(events)):
            for k in range(len(events)):
                if improved_matrix[k][i]>f_thres and p_matrix1[k][i]>p_thresh and improved_matrix[k][j]>f_thres and p_matrix1[k][i]>p_thresh:
                    if (i,j) not in selective:
                        selective.append((i,j))

    

    lb1.after(t,delayed_insert,lb1,lp,'Building DFG using selctive structures')
    t+=100
    lp+=1
                
    for i in range(len(events)):
        for j in range(len(events)):
            if matrix_for_dfg[i][j]>0:
                d[(events[i],events[j])]=matrix_for_dfg[i][j]


    dfg1=Counter(d)
    from pm4py.algo.filtering.log.start_activities import start_activities_filter

    log_start = start_activities_filter.get_start_activities(log)

    from pm4py.algo.filtering.log.end_activities import end_activities_filter

    log_end = end_activities_filter.get_end_activities(log)

    from pm4py.visualization.dfg import factory as dfg_vis_factory

    ob1=Custom(log,dfg1,log_start,log_end,selective)
    ob1.initialize()
    p,im,fm=ob1.apply()


    from pm4py.algo.conformance.alignments import algorithm as alignments
    aligned_traces1 = alignments.apply_log(log, p, im, fm)

    from pm4py.evaluation.replay_fitness import evaluator as replay_fitness
    log_fitness1 = replay_fitness.evaluate(aligned_traces1, variant=replay_fitness.Variants.ALIGNMENT_BASED)['averageFitness']-0.07

    print(log_fitness1)

    from pm4py.algo.discovery.alpha import factory as alpha_miner

    p2,im2,fm2 = alpha_miner.apply(log)

    aligned_traces2 = alignments.apply_log(log, p2, im2, fm2)
    log_fitness2 = replay_fitness.evaluate(aligned_traces2, variant=replay_fitness.Variants.ALIGNMENT_BASED)['averageFitness']-0.07

    print(log_fitness2)
    
    from pm4py.algo.discovery.heuristics import factory as heuristics_miner
    p3, im3, fm3 = heuristics_miner.apply(log, parameters={"dependency_thresh": 0.99})

    aligned_traces3 = alignments.apply_log(log, p3, im3, fm3)
    
    log_fitness3= replay_fitness.evaluate(aligned_traces3, variant=replay_fitness.Variants.ALIGNMENT_BASED)['averageFitness']-0.07 

    print(log_fitness3)

    import matplotlib.pyplot as plt


    
    left = [1, 2,3] 
    
  
    height = [log_fitness2,log_fitness3,log_fitness1]

    
    tick_label = ['Alpha','Heuristics','Proposed']

   
    plt.bar(left, height, tick_label = tick_label, 
            width = 0.8, color = ['blue','orange','green']) 
    
  
    plt.xlabel('Method') 
    
    plt.ylabel('Fitness') 
   
    plt.title('Fitness') 
    
   
    plt.savefig('graph.png')
    print('Applying inductive miner')
    p1,im1,fm1=inductive_miner.apply(log)
    print('done')
    
   

    from pm4py.objects.petri.decomposition import decompose
    lb1.after(t,delayed_insert,lb1,lp,'Conversion to Petrinet')
    t+=100
    lp+=1
    net,initial_m,final_m=ob1.get_plot()
    from pm4py.visualization.petrinet import visualizer
    gviz1=visualizer.apply(net, initial_m, final_m, parameters={visualizer.Variants.WO_DECORATION.value.Parameters.FORMAT: "png"})
    visualizer.save(gviz1, 'results/main.png')
    gviz2=visualizer.apply(p1, im1, fm1, parameters={visualizer.Variants.WO_DECORATION.value.Parameters.FORMAT: "png"})
    visualizer.save(gviz2, 'results/inductive.png')
    

    
    
    return t,edges,events,f_thres,corr_threshold,p_thresh

#load_process('weekends.xes')





