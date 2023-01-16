from fastapi import FastAPI, Query, HTTPException, Path
from models import Company
from typing import Optional
# from uuid import UUID, uuid4
import json

description = """
APIs list world techie companies. 🚀

## What you can do.

You can perform **crude operations on these APIs for testing purposes**.

## Users

You will be able to:

* **Get, Create, Update and Delete a Company ** .

"""

tags_metadata = [
    {
        "name": "teches",
        "description": "lists all world best tech companies.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]




app = FastAPI(
    title="Lists of World Tech Companies",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com",
    contact={
        "name": "Samuel",
        "url": "http://x-force.example.com/",
        "email": "",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=tags_metadata
)



# this help to read the comapany data

with open('payload.json', 'r') as f:
      company = json.load(f)
    #   print(company) 


# @app.get("/")
# def get_request():
#     return {"data": "Welcome to Top world tech companies list API"}



    # # # this get a single company
@app.get("/tech-api/get-all-listed",tags=["teches"], status_code=200)
async def get_all_company():
    return company


# # # this get a single company
@app.get("/tech-api/get-byId/{company_id}", tags=["teches"], status_code=200)
async def get_single_company(company_id: int):
    ck = [c for c in company if c['id'] == company_id]
    return ck[0] if len(company) > 0 else {}


# #post method 
@app.post("/tech-api/add-company",tags=["teches"], status_code=201)
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
# @app.get("/get-by-name", status_code =200)
# def search_company(company_name: Optional[str] = Query(None, title="Company Name", description="Search with company name" ), founder: Optional[str]  = Query(None, title="founder", description = "Search with Company founder" )):
    
#     comp1 = [h for h in company if h['company_name'] == company_name ]
   
#     if company_name is None:
#         if founder is None:
#             return company     
#         else:
#             return comp1         

#     else:
#         comp2 = [h for h in company if founder.lower() in h['founder'].lower()] 
#         if founder is None:
#            return comp2
#         else:
#            combined = [h for h in comp1 if h in comp2] 
#            return combined      


#update  method 
@app.put("/tech-api/update",tags=["teches"], status_code=204)
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
@app.delete("/tech-api/delete/{company_id}",tags=["teches"], status_code=204)
def remove_company(company_id: int):
    cp = [p for p in company if p['id'] == company_id]
    if len(cp) > 0:
        company.remove(cp[0])
        with open('payload.json', 'w') as f:
            json.dump(company, f)
    else:
        return HTTPException(status_code=404, detail=f"There is no company with {company_id} does not exist")
 



