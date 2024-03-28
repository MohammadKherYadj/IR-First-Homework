# -*- coding: utf-8 -*-
"""Y24_S2_IR_HW1.ipynb

# وظيفة 1:

Name: اسم_الطالب كنيته

ID: 00000000

## setup
"""

import pandas as pd

"""## Prepare classes

### Preprcessor

#### Task-1:
"""

#-preprocessor
class Preprocessor():
    @staticmethod
    def process(sentence):
        print("")
        #---------------------------
        # اكتب اجابتك هنا
        #return ...
        #---------------------------


    #---------------------------
    # اكتب توابع المعالجة المسبقة هنا
    # def ...
    #---------------------------

"""### TDIM

#### Task-2:

قم بالتعديل على باني الكلاس

IndexModel

بحيث يصبح نوع الفهرس المستخدم  من نمط معطيات جدول, أي

data type of the attribute "_index" is DataFrame
"""

#- Index Model : Term Document Incidence Matrix
class IndexModel:

    def __init__(self, documents_df):
        print("question-2.1")
        #---------------------------
        # اكتب اجابتك هنا
        #self._index = ...
        #---------------------------

    def term_incidence_vector(self, term):
        print("question-2.2")
        # اكتب اجابتك هنا
        #return ...

"""### Retriever"""

class Retriever:
    def __init__(self):
        self._terms_operator = ['&', '|', '~']

    def _merge(self, l1, l2):
        res = []
        i1 = 0; i2 = 0
        while i1 < len(l1) and i2 < len(l2):
            if l1[i1]==l2[i2]:
                res += [l1[i1]]
                i1 += 1; i2 += 1
            elif l1[i1]<l2[i2]:
                i1 += 1;
            elif l2[i2]<l1[i1]:
                i2 += 1;
        return res;

    def boolean_operator_processing(self, bop, prevS, nextS=None, docidlist=None):
        if bop == "&":
            return self._merge(prevS, nextS)
        elif bop=="|" :
            return list(set(prevS+nextS))
        elif bop == "~":
            return [a for a in docidlist if a not in prevS]

    def retrieve(self, query_terms, index_model):
        ret_docs = []
        bitwiseop=""
        result=[]
        has_previous_term=False
        has_not_operation=False
        inc_vec_prev=[]
        inc_vec_next=[]
        for term in query_terms:
            if term not in self._terms_operator:
                if has_not_operation:
                    if has_previous_term:
                        inc_vec_next=self.boolean_operator_processing(bop="~",prevS=index_model.term_postings(term),nextS=inc_vec_next, docidlist=index_model.getdi())
                    else :
                        inc_vec_prev=self.boolean_operator_processing(bop="~",prevS=index_model.term_postings(term),nextS=inc_vec_next, docidlist=index_model.getdi())
                        result=inc_vec_prev
                    has_not_operation=False
                elif has_previous_term:
                    inc_vec_next=index_model.term_postings(term)
                else:
                    inc_vec_prev=index_model.term_postings(term)
                    result= inc_vec_prev
                    has_previous_term=True
            elif term =="~":
                has_not_operation=True
            else:
                bitwiseop=term

            #----------
            if len(inc_vec_next)!= 0  :
                result = self.boolean_operator_processing(bop=bitwiseop,prevS=inc_vec_prev,nextS=inc_vec_next, docidlist=index_model.getdi())
                inc_vec_prev=result
                has_previous_term=True
                inc_vec_next= []

        #-----
        for res in result:
            ret_docs.append({'docno':res, 'score':1})
        ret_docs = pd.DataFrame(ret_docs, columns=['docno', 'score', 'content']).sort_values(by=['score'], ascending=False)
        return ret_docs

"""### search engine"""

class SearchEngine:
    def __init__(self, preprocessor, retriever, documents):
        self.preprocessor = preprocessor
        self.retriever = retriever
        self.documents = None
        self.model = None
        self.rebuild(documents)

    def rebuild(self, documents):
        self.documents = documents
        self.documents['ntext'] = self.documents['text'].apply(self.preprocessor.process)
        self.model = IndexModel(self.documents)

    def querying(self, query):
        query_terms = self.preprocessor.process(query)
        docs_res = self.retriever.retrieve(query_terms, self.model)
        if docs_res.shape[0]>0:
            docs_res['content'] = docs_res.apply(
                lambda row: self.documents[self.documents['id']==row.id]['text'].iloc[0], axis = 1)
        return docs_res

"""## Build and use the IRS

#### Task-3:

انشئ جدول وثائق من مجموعة العبارات التالية


1. برنامج تعليمي للغة الإنجليزية ومسار سريع
2. تعلم الفهرسة الدلالية الكامنة
3. الكتاب في الفهرسة الدلالية
4. التقدم في البنية والفهرسة الدلالية
5. تحليل تحليل البنية الكامنة
"""

# اكتب اجابتك هنا
#df = ...

"""#### Task-4:

انشئ كيان من نظام محرك البحث
"""

# اكتب اجابتك هنا
#ir_sys = ...

"""#### Task-5:

اعرض اخر 3 وثائق

واعرض حجم المصفوفة TDIM
"""

# اخر 3 وثائق
# اكتب اجابتك هنا
#...

# حجم مصفوفة وجود الكلمات في الوثائق TDIM
# اكتب اجابتك هنا
#...

"""#### Task-6:

قم بعرض الوثائق الموافقة للاستعلامات التالية

Query-1 = "التقدم & البنية & ~ تحليل"
"""

# اكتب اجابتك هنا
#...

"""Query-2 = "الكامنة & ~ تعليمي"
"""

# اكتب اجابتك هنا
#...

"""Query-3 = "التقدم والبنية بدون تحليل"
"""

# اكتب اجابتك هنا
#...

"""Query-4 = "تعلم | تحليل & الكامنة"

"""

# اكتب اجابتك هنا
#...

