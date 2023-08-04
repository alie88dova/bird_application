import json
import re
from ru.travelfood.simple_ui import SimpleSQLProvider as sqlClass


test_data = {}


def on_start(hashMap,_files=None,_data=None):

   hashMap.put("SQLConnectDatabase","db.DB")
   
   hashMap.put("SQLExec",json.dumps({"query":"create table IF NOT EXISTS Bird(id integer primary key autoincrement,art text, name text, color text)","params":""}))

   return hashMap


def bird_on_init(hashMap,_files=None,_data=None):
 
   list = { "customcards":         {
        
            "layout": {
            "type": "LinearLayout",
            "orientation": "vertical",
            "height": "match_parent",
            "width": "match_parent",
            "weight": "0",
            "Elements": [
                {
                    "type": "TextView",
                    "show_by_condition": "",
                    "Value": "@bird_name",
                    "NoRefresh": False,
                    "document_type": "",
                    "mask": "",
                    "Variable": ""
                },
                
                {
                    "type": "TextView",
                    "show_by_condition": "",
                    "Value": "@bird_color",
                    "NoRefresh": False,
                    "document_type": "",
                    "mask": "",
                    "Variable": ""
                }
                ]
                }
        
    }
    }
  

   sql = sqlClass()
   res = sql.SQLQuery("select * from Bird","")
   
   records = json.loads(res)
   
   list["customcards"]["cardsdata"]=[]
   for record in records:
      list["customcards"]["cardsdata"].append({"key":record['id'],"bird_name":record['name'],"bird_color":record['color']})
   hashMap.put("cards",json.dumps(list))
   
   return hashMap
 


def bird_clicks(hashMap,_files=None,_data=None):
   if hashMap.get("listener")=="btn_add_bird":
      hashMap.put("ShowScreen", "Добавление птицы")
   elif hashMap.get("listener")=="CardsClick":
      hashMap.put("toast",str(hashMap.get("selected_card_key")))
      jlist = json.loads(hashMap.get("cards"))
      goodsarray = jlist["customcards"]['cardsdata']
        
      jrecord = next(item for item in goodsarray if str(item["key"]) == hashMap.get("selected_card_key"))

      hashMap.put("s_card_name",jrecord['bird_name'])
      hashMap.put("s_card_color",jrecord['bird_color'])

      hashMap.put("ShowScreen", "Карточка птицы")




def input_on_crBird(hashMap,_files=None,_data=None):
   if hashMap.get("listener") == "btn_create_bird":
      sql = sqlClass()
      success=sql.SQLExec("insert into Bird(name,color) values(?,?)",f"{hashMap.get('bird_name')},{hashMap.get('bird_color')}") 
      if success:
         hashMap.put("ShowScreen","Вывод птиц")
         hashMap.put("toast","Добавлено")  
   
   return hashMap