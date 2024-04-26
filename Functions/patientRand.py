def patientRand(G, s, irrs, d):
  '''
  Function to generate a simulated medical patient profile (randomizing a set of symptoms and already known diseases) and:
  - ensuring that a specified number of symptoms are all related to at least one disease
  - ensuring that a specified number of secondary symptoms are not related to any disease which is in common to all the above relevant symptoms
    (irrelevant symptoms to mimic real-world complexity in medical diagnosis)
  - also returning the set of possible diagnoses based on the relevant symptoms' common relations to diseases
  - - -
  Inputs:
    G: the medical knowledge graph of reference (in NetworkX multiDiGraph format)
    s: the number of relevant symptoms to randomize (0 < s)
    irrs: the number of irrelevant symptoms to randomize (0 <= irrs)
    d: the number of already known diseases to randomize (0 <= d < # of diseases in G)
  Outputs:
    patient: a dictionary containing a 'symptoms' list (with randomly selected relevant/irrelevant symptoms, in this order) and a 'diseases' list
             (the number of relevant/irrelevant symptoms randomized could be lower than asked, due to the specified constraints)
    possibleDiseases: set of all possible reasonable diagnoses based on the randomized relevant symptoms
  - - -
  '''
  
  import random

  # Checking for input significance
  s = max(1, s)  
  irrs = max(0, irrs)
  d = min(max(0, d), len([node for node, attr in G.nodes(data=True) if attr['kind'] == 'Disease']))

  # Selection of one main symptom
  symptoms = [random.choice([node for node, attr in G.nodes(data=True) if attr['kind'] == 'Symptom' and len(list(G.predecessors(node))) > 0])]  # chosing first symptom among the ones connected to at least one disease (some symptoms are otherwise disconnected nodes)
  possibleDiseases = set(G.predecessors(symptoms[0])) # getting all diseases connected to the main symptom
  possibleSymptoms = {possibleSymptom for possibleDisease in possibleDiseases for possibleSymptom in G.neighbors(possibleDisease) if possibleSymptom[:7]=='Symptom'} - set(symptoms)  # getting all symptoms connected to at least one possible disease

  # Selection of up to s-1 additional relevant symptoms (all connected to at least one disease also connected to the other relevant symptoms)
  for n in range(s-1):
    if len(possibleSymptoms) == 0:
      break
    symptoms = symptoms + [random.choice(list(possibleSymptoms))]
    possibleDiseases = possibleDiseases & {disease for disease in G.predecessors(symptoms[-1])}
    possibleSymptoms = {possibleSymptom for possibleDisease in possibleDiseases for possibleSymptom in G.neighbors(possibleDisease) if possibleSymptom[:7]=='Symptom'} - set(symptoms)  # excluding all already chosen symptoms

  # Selecting up to irrs irrelevant symptoms disconnected from all the remaining possible diseases
  possibleIrrelevantSymptoms = {node for node, attr in G.nodes(data=True) if attr['kind'] == 'Symptom'} - possibleSymptoms - set(symptoms)  # excluding symptoms connected to at least one possible disease
  for n in range(irrs):
    if len(possibleIrrelevantSymptoms) == 0:
      break
    symptoms = symptoms + [random.choice(list(possibleIrrelevantSymptoms))]
    possibleIrrelevantSymptoms = possibleIrrelevantSymptoms - {symptoms[-1]}

  # Selecting d diseases already diagnosed to the patient
  diseases = random.sample([node for node, attr in G.nodes(data=True) if attr['kind'] == 'Disease'], d)

  # Building the patient's dictionary-representation
  patient = {'symptoms': symptoms, 'diseases': diseases}

  return patient, possibleDiseases