from fastapi import FastAPI
from routes.RoleRoutes import router as role_router
from routes.UserRoutes import router as user_router
from routes.StateRoutes import router as state_router
from routes.CityRoutes import router as city_router
from routes.AreaRoutes import router as area_router
from routes.CategoryRoutes import router as category_router
from routes.SubCategoryRoutes import router as sub_category_router
from routes.PropertyRoutes import router as property_router
from routes.InquiryRoutes import router as inquiry_router


# import cors middleware
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# app.include_router(role_router)
app.include_router(role_router, prefix="/api", tags=["Roles"])
app.include_router(user_router, prefix="/api", tags=["Users"])
# app.include_router(user_router)
app.include_router(state_router, prefix="/api" ,tags=["States"])
app.include_router(city_router, prefix="/api",tags=["Cities"])
app.include_router(area_router,prefix="/api",tags=["Areas"])
app.include_router(category_router,prefix="/api",tags=["Categories"])

app.include_router(sub_category_router,prefix="/api",tags=["SubCategories"])
app.include_router(property_router,prefix="/api",tags=["Properties"])
app.include_router(inquiry_router,prefix="/api",tags=["Inquiries"])
# app.include_router(property_router)




