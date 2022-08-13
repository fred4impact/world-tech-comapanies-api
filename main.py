from fastapi import FastAPI, Query, HTTPException
from models import Company
from typing import Optional
# from uuid import UUID, uuid4
import json


app = FastAPI()


# this help to read the comapany data

with open('payload.json', 'r') as f:
      company = json.load(f)
    #   print(company) 


@app.get("/")
def get_request():
    return {"data": "Welcome to Top world tech companies list API"}


# # # this get a single company
@app.get("/company/{company_id}")
async def get_single_company(company_id: int):
    ck = [c for c in company if c['id'] == company_id]
    return ck[0] if len(company) > 0 else {}


# #post method 
@app.post("/company", status_code=201)
def add_company(comp: Company):
    company_id = max([r['id'] for r in company]) + 1
    new_company = {
       "id": company_id,
       "company_name": comp.company_name,
       "founder": comp.founder,
       "year_established": comp.year_established,
       "current_networth": comp.current_networth,
       "hq": comp.hq,
       "country": comp.country
    }

    company.append(new_company)

    with open('payload.json', 'w') as f:
      json.dump(company, f)

    return new_company    

# #search fucntion  using company_name or founder
@app.get("/search", status_code =200)
def search(company_name: Optional[str] = Query(None, title="company_name", description="Search with company name" ), founder: Optional[str]  = Query(None, title="founder", description = "Search with founder" )):
    
    comp1 = [h for h in company if h['company_name'] == company_name ]
   
    if company_name is None:
        if founder is None:
            return company     
        else:
            return comp1         

    else:
        comp2 = [h for h in company if founder.lower() in h['founder'].lower()] 
        if founder is None:
           return comp2
        else:
           combined = [h for h in comp1 if h in comp2] 
           return combined      


#update  method 
@app.put("/company", status_code=204)
def update_company(updatecomp: Company):
    new_update = {
     "id": updatecomp.id,
     "company_name": updatecomp.company_name,
     "year_esterblished": updatecomp.year_established,
     "current_networth": updatecomp.current_networth,
     "hq": updatecomp.hq,
     "country": updatecomp.country
    }

    company_list = [r for r in company if r['id'] == updatecomp ]
    if len(company_list) > 0:
        company.remove(company_list[0])
        company.append(new_company)
        with open('payload.json', 'w') as f:
            json.dump(company, f)
        return new_company
    else:
        return HTTPException(status_code=404, detail=f"Company with {updatecomp.id} does not exist")


# delete company
@app.delete("/company/{company_id}", status_code=204)
def remove_company(company_id: int):
    cp = [p for p in company if p['id'] == company_id]
    if len(cp) > 0:
        company.remove(cp[0])
        with open('payload.json', 'w') as f:
            json.dump(company, f)
    else:
        return HTTPException(status_code=404, detail=f"There is no company with {company_id} does not exist")
 

