# Automation Coverage

## Source analysis

The workbook reports 102 master test cases across Signup, Login, Logout, Session, Home Page, Product Details, Add to Cart, Cart, Purchase, and Contact Form. The workbook marks 71 cases `Yes`, 30 `No`, and TC028 `No (multi-step transactional flow)`. All 71 `Yes` cases are implemented.

| Measure | Count |
|---|---:|
| Total Excel test cases | 102 |
| Automated | 71 |
| Not automated | 31 |
| Positive candidates | 20 workbook summary baseline |
| Negative candidates | 15 workbook summary baseline |
| Boundary candidates | 10 workbook summary baseline |
| Edge candidates | 9 workbook summary baseline |
| Security candidates | 7 workbook summary baseline |
| Regression candidates | 31 workbook summary baseline |
| Known bugs with regression coverage | 13 represented in automated candidates |

## Not automated

These remain manual because the workbook marks them `No`, or explicitly excludes the transactional flow. Reasons are retained rather than silently omitted: responsive/accessibility observations, rapid-click/browser lifecycle behavior, extended multi-step purchase validation, or exploratory UI/usability checks requiring specialist review.

`TC028, TC036, TC038, TC046, TC048, TC050, TC051, TC052, TC059, TC060, TC061, TC063, TC064, TC068, TC074, TC077, TC078, TC079, TC084, TC086, TC087, TC088, TC089, TC090, TC091, TC096, TC097, TC098, TC099, TC101, TC102`

The exact scenario text and candidate decision are preserved in the supplied workbook. TC028 is the multi-step transactional flow exclusion.

## Module coverage

| Module | Automated IDs |
|---|---|
| Signup | TC001-TC008, TC018, TC021, TC031-TC035 |
| Login | TC009-TC017, TC019-TC020, TC037, TC039-TC042, TC095 |
| Home Page | TC022-TC024, TC049, TC053 |
| Add to Cart | TC025-TC027 |
| Purchase | TC029-TC030, TC065-TC076 |
| Logout/Session | TC043-TC045, TC047 |
| Product Details | TC054, TC100 |
| Cart | TC055-TC058, TC062, TC094 |
| Contact Form | TC080-TC083, TC085, TC092-TC093 |

Known defect references are retained as pytest markers and in `data/known_bugs.py`.
