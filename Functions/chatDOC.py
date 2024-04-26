def chatDOC (G, patient):
  '''
  Function to analyze an hypothetical patient situation starting from suffered symptoms and eventually already diagnosed diseases in order to:
  - when possible, obtain a univocal diagnosis of the responsible disease, indicating relevant revealing symptoms and known diseases and
    the diagnosed disease's additional verifiable symptoms, affected anatomies and (eventually) associated compounds viable for the treatment
  OR
  - when no univocal diagnosis seems possible, a list of possible diseases correlated with the suffered symptoms and known diseases
  - - -
  Inputs:
    G: the medical knowledge graph of reference (in NetworkX multiDiGraph format)
    patient: a dictionary with a 'symptoms' lists and a 'diseases' list containing the already known patient's elements to be analyzed
            OR
             None, in order to activate the input-output mode and progressively insert data chatting with a the 'virutal DOC'
  Outputs:
    Diagnosis: a dictionary containing all input symptoms and diseases classified by relevance and the related univocal/imprecise diagnosis
               (unknown data set to None values)
  - - -
  '''

  import networkx as nx
  from mdgJaccard import mdgJaccard

  # Eventual activation of input-output chat mode if patient == None
  IO = True
  if patient != None:
    IO = False

  # Individuation of the main symptom
  if IO:
    symptoms = ['initialization']
    while len(symptoms) == 0 or symptoms == ['initialization']:
      if symptoms == ['initialization']:
        mainSymptom = input("Hi! How can I help you today? Which is your main symptom?\t").strip()
      else:
        mainSymptom = input("Main symptom not recognized, please insert the name or id of the main symptom you are experimenting:\t").strip()
      if mainSymptom in G.nodes() and mainSymptom[:7]=='Symptom':
        symptoms = [mainSymptom]
      else:
        symptoms = [id for id,attr in G.nodes(data=True) if mainSymptom.lower() in attr['name'].lower() and attr['kind'] == 'Symptom' and len(mainSymptom) > 2]
    if len(symptoms) > 1:
      print("There are", len(symptoms), "symptoms related to your description:")
      for i in range(len(symptoms)):
        print(i+1, "-", G.nodes[symptoms[i]]['name'])
      selection = -1
      while not 0<=selection<len(symptoms):
        try:
          selection = int(input("Please select the number of the main symptom you are actually experimenting:\t").strip())-1
          if not 0<=selection<len(symptoms):
            print("Invalid slection, please input the number corresponding to the symptom of interest as from the above list!")
        except:
          print("Input not recognized as a number, please input the number corresponding to the symptom of interest as from the above list!")
      symptoms = [symptoms[selection]]
    print("Your main symptom is then:", G.nodes[symptoms[0]]['name'], "!")
  else:
    symptoms = patient['symptoms']
    if not (symptoms[0] in G.nodes() and symptoms[0][:7]=='Symptom'):
      symptoms[0] = [id for id,attr in G.nodes(data=True) if symptoms[0].lower() == attr['name'].lower() and attr['kind'] == 'Symptom'][0]
    if not (symptoms[0] in G.nodes() and symptoms[0][:7]=='Symptom'):
      return "Main symptom not recognized!"

  # Initializing the search for the disease
  possibleDiseases = set(G.predecessors(symptoms[0]))
  possibleSymptoms = {possibleSymptom for possibleDisease in possibleDiseases for possibleSymptom in G.neighbors(possibleDisease) if possibleSymptom[:7]=='Symptom'}

  # Asking for eventually already recognized secondary symptoms, which could be correlated to the main one and reveal the actual disease
  relevantSymptoms = {symptoms[0]}
  irrelevantSymptoms = set()
  unrecognizedSymptoms = set()
  if len(possibleDiseases)>1 or not IO:
    doResearch = False
    if IO:
      YN = input("Do you already recognize specific other symptoms?\t[Y/N]\t").lower()
      while YN not in ['y', 'yes','n','no']:
        print("Input not recognized, please just answer yes or no to the following question!")
        YN = input("Do you already recognize specific other symptoms?\t[Y/N]\t").lower()
      if YN in ['y', 'yes']:
        secondarySymptoms = [x.strip() for x in input("Please specify all already recognized secondary symptoms ordered by relevance and separated by commas:\t").split(sep=',')]
        doResearch = True
    elif not IO:
      secondarySymptoms = symptoms[1:]
    if not IO or doResearch:
      for symptom in secondarySymptoms:
        if symptom in G.nodes() and symptom[:7]=='Symptom':
          relevantSymptom = symptom
        else:
          if IO:
            symptomIDs = list({id for id,attr in G.nodes(data=True) if symptom.lower() in attr['name'].lower() and attr['kind'] == 'Symptom'} - (relevantSymptoms | irrelevantSymptoms))
          else:
            symptomIDs = list({id for id,attr in G.nodes(data=True) if symptom.lower() == attr['name'].lower() and attr['kind'] == 'Symptom'} - (relevantSymptoms | irrelevantSymptoms))
          if len(symptomIDs) == 0 or len(symptom) < 3 or (not IO and len(symptomIDs) > 1):
            unrecognizedSymptoms = unrecognizedSymptoms | {symptom}
            continue
          elif len(symptomIDs) == 1:
            relevantSymptom = symptomIDs[0]
          elif IO:
            print("There are ", len(symptomIDs), " symptoms related to your description '", symptom, "':", sep = '')
            for i in range(len(symptomIDs)):
              print(i+1, "-", G.nodes[symptomIDs[i]]['name'])
            selection = -1
            while not 0<=selection<len(symptomIDs):
              try:
                selection = int(input("Please select the number of the secondary symptom you are actually experimenting:\t").strip())-1
                if not 0<=selection<len(symptomIDs):
                  print("Invalid slection, please input the number corresponding to the symptom of interest as from the above list!")
              except:
                print("Input not recognized as a number, please input the number corresponding to the symptom of interest as from the above list!")
            relevantSymptom = symptomIDs[selection]
        if IO and relevantSymptom in symptoms:
          continue
        if IO:
          symptoms = symptoms + [relevantSymptom]
        else:
          symptoms[symptoms.index(symptom)] = relevantSymptom
        if relevantSymptom in possibleSymptoms:
          relevantSymptoms = relevantSymptoms | {relevantSymptom}
          possibleDiseases = possibleDiseases & {disease for disease in G.predecessors(relevantSymptom)}
          possibleSymptoms = {possibleSymptom for possibleDisease in possibleDiseases for possibleSymptom in G.neighbors(possibleDisease) if possibleSymptom[:7]=='Symptom'} - (relevantSymptoms | irrelevantSymptoms)
        else:
          irrelevantSymptoms = irrelevantSymptoms | {relevantSymptom}
      if IO and len(unrecognizedSymptoms) > 0:
        print("The following inputs are not recognizable as symptoms:", '; '.join(unrecognizedSymptoms), "!")
      if IO and len(irrelevantSymptoms) > 0:
        print("The following symptoms you described seem to be uncorrelated to the main ones: ", '; '.join([G.nodes[symptom]['name'] for symptom in irrelevantSymptoms]), "!")
  inputSymptoms = len(symptoms)

  # Asking for eventually already diagnosticated diseases, causing symptoms which could be correlated to the searched disease too
  unrecognizedDiseases = set()
  diseases = []
  if not IO:
    diseases = patient['diseases']
    secondaryDiseases = patient['diseases']
  if len(possibleDiseases) > 1 or not IO:
    doResearch = False
    if IO:
      YN = input("Have you already been diagnosed with other diseases?\t[Y/N]\t").lower()
      while YN not in ['y', 'yes','n','no']:
        print("Input not recognized, please just answer yes or no to the following question!")
        YN = input("Have you already been diagnosed with other diseases?\t[Y/N]\t").lower()
      if YN in ['y', 'yes']:
        secondaryDiseases = [x.strip() for x in input("Please specify all already diagnosed diseases ordered by relevance and separated by commas:\t").split(sep=',')]
        doResearch = True
    if not IO or doResearch:
      for disease in secondaryDiseases:
        if disease in G.nodes() and disease[:7]=='Disease':
          relevantDisease = disease
        else:
          if IO:
            diseaseIDs = list({id for id,attr in G.nodes(data=True) if disease.lower() in attr['name'].lower() and attr['kind'] == 'Disease'}-set(diseases))
          else:
            diseaseIDs = list({id for id,attr in G.nodes(data=True) if disease.lower() == attr['name'].lower() and attr['kind'] == 'Disease'}-set(diseases))
          if len(diseaseIDs) == 0 or len(disease) < 3 or (not IO and len(symptomIDs) > 1):
            unrecognizedDiseases = unrecognizedDiseases | {disease}
            continue
          elif len(diseaseIDs) == 1:
            relevantDisease = diseaseIDs[0]
          elif IO:
            print("There are ", len(diseaseIDs), " diseases related to your description '", disease, "':", sep = '')
            for i in range(len(diseaseIDs)):
              print(i+1, "-", G.nodes[diseaseIDs[i]]['name'])
            selection = -1
            while not 0<=selection<len(diseaseIDs):
              try:
                selection = int(input("Please select the number of the disease you have actually beign diagnosed with:\t").strip())-1
                if not 0<=selection<len(diseaseIDs):
                  print("Invalid slection, please input the number corresponding to the disease of interest as from the above list!")
              except:
                print("Input not recognized as a number, please input the number corresponding to the disease of interest as from the above list!")
            relevantDisease = diseaseIDs[selection]
        if IO and relevantDisease in diseases:
          continue
        if IO:
          diseases = diseases + [relevantDisease]
        else:
          diseases[diseases.index(disease)] = relevantDisease
        relevantDiseaseSymptoms = [symptom[0] for symptom in sorted([(symptom, len(list(G.predecessors(symptom)))) for symptom in G.neighbors(relevantDisease) if symptom[:7]=='Symptom'], key = lambda x: x[1])]
        symptoms = symptoms + [symptom for symptom in relevantDiseaseSymptoms if symptom not in symptoms]
        for relevantSymptom in relevantDiseaseSymptoms:
          if relevantSymptom in possibleSymptoms:
            relevantSymptoms = relevantSymptoms | {relevantSymptom}
            possibleDiseases = possibleDiseases & {disease for disease in G.predecessors(relevantSymptom)}
            possibleSymptoms = {possibleSymptom for possibleDisease in possibleDiseases for possibleSymptom in G.neighbors(possibleDisease) if possibleSymptom[:7]=='Symptom'} - (relevantSymptoms | irrelevantSymptoms)
          else:
            irrelevantSymptoms = irrelevantSymptoms | {relevantSymptom}
      if IO and len(unrecognizedDiseases) > 0:
        print("The following inputs are not recognizable as diseases:", '; '.join(unrecognizedDiseases), "!")
      if IO and len(irrelevantSymptoms) > 0:
        print("The following symptoms you are experiencing seem to be uncorrelated to the main ones: ", '; '.join([G.nodes[symptom]['name'] for symptom in irrelevantSymptoms]), "!")

  # Asking for eventually recognizable secondary symptoms (proposing them on an inverse-similarity basis wrt the main one), which could reveal the actual disease
  if IO and len(possibleDiseases) > 1:
    possibleSymptomsSimilarity = sorted([(possibleSymptom, mdgJaccard(G, possibleSymptom, symptoms[0])) for possibleSymptom in possibleSymptoms], key = lambda x: x[1])
    i = 0
    while i < 5 and len(possibleDiseases) > 1:
      YN = input("Do you maybe feel this symptom too?\t" + G.nodes[possibleSymptomsSimilarity[i][0]]['name'] + "\t[Y/N]\t").lower()
      while YN not in ['y', 'yes','n','no']:
        print("Input not recognized, please just answer yes or no to the following question!")
        YN = input("Do you maybe feel this symptom too?\t" + G.nodes[possibleSymptomsSimilarity[i][0]]['name'] + "\t[Y/N]\t").lower()
      if YN in ['y', 'yes']:
        symptoms = symptoms + [possibleSymptomsSimilarity[i][0]]
        possibleDiseases = possibleDiseases & set(G.predecessors(possibleSymptomsSimilarity[i][0]))
      i += 1

  # Outputting results
  relevantDiseases = {disease for disease in diseases if len({symptom for symptom in G.neighbors(disease) if symptom[:7] == 'Symptom'} & {symptom for disease in possibleDiseases for symptom in G.neighbors(disease) if symptom[:7] == 'Symptom'}) > 0}
  irrelevantDiseases = set(diseases) - relevantDiseases
  if len(possibleDiseases) == 1:
    diagnosis = list(possibleDiseases)[0]
    orderedDiagnosisSymptoms = [item[0] for item in sorted({symptom:G.in_degree(symptom) for symptom in ({symptom for symptom in G.neighbors(diagnosis) if symptom[:7]=='Symptom'})}.items(), key=lambda x:x[1])]
    orderedAdditionalSymptoms = [symptom for symptom in orderedDiagnosisSymptoms if symptom not in (relevantSymptoms | irrelevantSymptoms)]
    orderedAnatomies = [item[0] for item in sorted([(anatomy,G.in_degree(anatomy)) for anatomy in G.neighbors(diagnosis) if anatomy[:7]=='Anatomy'], key=lambda x:x[1])]
    orderedCompounds_sideEffectsNum = sorted([(compound,len([sideEffect for sideEffect in G.neighbors(compound) if sideEffect[:11] == 'Side Effect'])) for compound in G.predecessors(diagnosis) if compound[:8] == 'Compound'], key=lambda x:x[1])
    orderedPharmacologicClasses = None
    if len(orderedCompounds_sideEffectsNum) > 0:
      orderedPharmacologicClasses = [phClass[0] for phClass in sorted([(phClass,len(list(G.neighbors(phClass)))) for phClass in G.predecessors(orderedCompounds_sideEffectsNum[0][0]) if phClass[:19]=='Pharmacologic Class'], key=lambda x:x[1])]
    orderedPossibleDiseases = None
  else:
    orderedPossibleDiseases = [disease[0] for disease in sorted([(disease,len([preDiagnosis for preDiagnosis in (set(G.neighbors(disease)) | set(G.predecessors(disease))) if preDiagnosis in diseases])) for disease in possibleDiseases], key=lambda x:-x[1])]
    diagnosis = None
    orderedDiagnosisSymptoms = None
    orderedAdditionalSymptoms = None
    orderedAnatomies = None
    orderedCompounds_sideEffectsNum = None
    orderedPharmacologicClasses = None
  if IO:
    print("The relevant symptoms are:", '; '.join([G.nodes[symptom]['name'] for symptom in symptoms if symptom in relevantSymptoms]), "!")
    if diagnosis != None:
      print("You may have this disease:", G.nodes[diagnosis]['name'])
      print("Therefore, you may also recognize the following main symptoms:", '; '.join([G.nodes[symptom]['name'] for symptom in orderedAdditionalSymptoms[:min(5,len(orderedAdditionalSymptoms))]]), "!")
      print("The main affected anatomies could be:", '; '.join(G.nodes[anatomy]['name'] for anatomy in orderedAnatomies[:min(5,len(orderedAnatomies))]), "!")
      print("There are", len(orderedCompounds_sideEffectsNum), "compounds that may treat the disease!")
      if len(orderedCompounds_sideEffectsNum) > 0:
        print("The suggested compound is:", G.nodes[orderedCompounds_sideEffectsNum[0][0]]['name'], "(with", orderedCompounds_sideEffectsNum[0][1], "side effects)!")
        if len(orderedPharmacologicClasses)==1:
          print("The relevant pharmacologic class is:", G.nodes[orderedPharmacologicClasses[0]]['name'], "!")
        elif len(orderedPharmacologicClasses)>1:
          print("The relevant pharmacologic classes are:", '; '.join([G.nodes[pharmacologicClass]['name'] for pharmacologicClass in orderedPharmacologicClasses[:min(5,len(orderedPharmacologicClasses))]]), "!")
    else:
      print("Thus your disease may be one of the following:", '; '.join([G.nodes[disease]['name'] for disease in orderedPossibleDiseases[:min(5,len(orderedPossibleDiseases))]]), "!")

  return {'symptoms':symptoms[:inputSymptoms], 'diseases':diseases, 'diseasesAdditionalSymptoms':symptoms[inputSymptoms:], 'relevantSymptoms':[symptom for symptom in symptoms if symptom in relevantSymptoms], 'irrelevantSymptoms':[symptom for symptom in symptoms if symptom in irrelevantSymptoms], 'unrecognizedSymptoms':[symptom for symptom in symptoms if symptom in unrecognizedSymptoms], 'relevantDiseases':relevantDiseases, 'irrelevantDiseases':irrelevantDiseases, 'unrecognizedDiseases':[disease for disease in diseases if disease in unrecognizedDiseases], 'possibleDiseases': orderedPossibleDiseases, 'diagnosis':diagnosis, 'diagnosisSymptoms':orderedDiagnosisSymptoms, 'additionalSymptoms':orderedAdditionalSymptoms, 'anatomies':orderedAnatomies, 'compounds_sideEffectsNum':orderedCompounds_sideEffectsNum, 'bestCompoundPharmacologicClasses':orderedPharmacologicClasses}


def visualizeDOC (DOCoutput):
  '''
  Function to graphically visualize outputs of the chatDOC function
  - - -
  Inputs:
    DOCoutput: a dictionary containing all input symptoms and diseases classified by relevance and the related univocal/imprecise diagnosis
  Outputs:
    Visualization: an image representation in NetworkX graph-drawing style of the input chatDOC diagnosis
  - - -
  '''

  # TODO: insert code

  return None