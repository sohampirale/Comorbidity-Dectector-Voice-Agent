cci_indexes=[
  {
    "condition": "Myocardial infarction",
    "variable": "MI",
    "points": 1,
    "notes": ""
  },
  {
    "condition": "Congestive heart failure",
    "variable": "CHF",
    "points": 1,
    "notes": ""
  },
  {
    "condition": "Peripheral vascular disease or bypass",
    "variable": "PVD",
    "points": 1,
    "notes": ""
  },
   {
    "condition": "Peripheral vascular disease or bypass",
    "variable": "PVD",
    "points": 1,
    "notes": ""
  },
  {
    "condition": "Cerebrovascular disease",
    "variable": "CVA",
    "points": 1,
    "notes": "CVA only"
  },
   {
    "condition": "Transient ischemic disease",
    "variable": "CVA",
    "points": 1,
    "notes": "CVA only"
  },
  {
    "condition": "Hemiplegia",
    "variable": "PLEGIA",
    "points": 2,
    "notes": "If hemiplegia, do not count CVA separately"
  },
  {
    "condition": "Pulmonary disease",
    "variable": "COPD",
    "points": 1,
    "notes": ""
  },
   {
    "condition": "Asthma",
    "variable": "COPD",
    "points": 1,
    "notes": ""
  },
  {
    "condition": "Diabetes",
    "variable": "DM",
    "points": 1,
    "notes": "DM only"
  },
  {
    "condition": "Diabetes with end organ damage",
    "variable": "DMENDORGAN",
    "points": 2,
    "notes": "If end organ damage, do not count DM separately"
  },
  {
    "condition": "Renal disease",
    "variable": "RENAL",
    "points": 2,
    "notes": ""
  },
  {
    "condition": "Mild liver disease",
    "variable": "MILD_LIVER",
    "points": 2,
    "notes": ""
  },
  {
    "condition": "Severe liver disease",
    "variable": "SEVERE_LIVER",
    "points": 3,
    "notes": ""
  },
  {
    "condition": "Peptic ulcer",
    "variable": "ULCER",
    "points": 1,
    "notes": ""
  },
   {
    "condition": "Gastric",
    "variable": "ULCER",
    "points": 1,
    "notes": ""
  },
  {
    "condition": "Cancer (lymphoma, leukemia, solid tumor)",
    "variable": "CANCER",
    "points": 2,
    "notes": "Nonmetastatic cancer only"
  },
  {
    "condition": "Metastatic solid tumor",
    "variable": "METASTASES",
    "points": 6,
    "notes": "If metastatic, do not count cancer separately"
  },
  {
    "condition": "Alzheimer",
    "variable": "DEMENTIA",
    "points": 1,
    "notes": ""
  },
    {
    "condition": "Dementia",
    "variable": "DEMENTIA",
    "points": 1,
    "notes": ""
  },
  {
    "condition": "Connective tissue disease",
    "variable": "RHEUMATIC",
    "points": 1,
    "notes": ""
  },
    {
    "condition": "Rheumatic",
    "variable": "RHEUMATIC",
    "points": 1,
    "notes": ""
  },
  {
    "condition": "AIDS",
    "variable": "AIDS",
    "points": 6,
    "notes": ""
  },
   {
    "condition": "HIV",
    "variable": "HIV",
    "points": 6,
    "notes": ""
  },
  {
    "condition": "Hypertension",
    "variable": "HBP",
    "points": 1,
    "notes": ""
  },
  {
    "condition": "Cellulitis",
    "variable": "SKIN_ULCER",
    "points": 2,
    "notes": ""
  },
   {
    "condition": "Skin ulcers",
    "variable": "SKIN_ULCER",
    "points": 2,
    "notes": ""
  },
  {
    "condition": "Depression",
    "variable": "DEPRESSION",
    "points": 1,
    "notes": ""
  },
  {
    "condition": "Warfarin use",
    "variable": "WARFARIN",
    "points": 1,
    "notes": ""
  }
]


print(len(cci_indexes))

#"condition": "Cerebrovascular disease or transient ischemic disease",
#    "condition": "Pulmonary disease / asthma",
#    "condition": "Gastric or peptic ulcer",
#    "condition": "Dementia or Alzheimer’s",
#    "condition": "Rheumatic or connective tissue disease",
#    "condition": "HIV or AIDS",
#    "condition": "Skin ulcers / cellulitis",


