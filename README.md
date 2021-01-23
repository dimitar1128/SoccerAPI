# Toptal Soccer
Last updated: 2021-01-23
## 1. Description
This is a api server for football/soccer fans to create fantasy teams and manage their teams including authentication,
visit their teams, set players on the transfer list, buy new players from the transfer list etc.
This supports an administrator role to manage all assets on the system.
Api endpoints and their details can be found in part 3.

##2. Technical stacks
- Language: Python
- Framework: DjangoResFramework
- Database: MySQL

## 3. API details
##### Note: All `RES_OK_*` and `RES_ERR_*` in the content of api response are result code constants (json format) and their details can be found in part 5 
### 3.1 Signup
This registers a new user with its email and password. When user signs up, it creates a team for the user.
Team has its `name`, `country` and `extra_value (5000000)` 
to buy new players, and 20 members (3 Goal Keepers, 6 Defenders, 6 Midfielders, 5 attackers).
A member has its `first_name`, `last_name`, `country`, `age (18-40)`, `value (1000000)`.
All the above values are generated automatically.
All automatically generated names are human-readable.

* **URL**

    /signup/

* **Method**
  
    POST
  
* **Data params**
    - email
        
        (required) Email of the new user.
    - password
        
        (required) Password of the new user.
        
* **Success Response**    
    * **Code:** 201 <br />
    **Content:** `RES_OK_USER_CREATED` <br />
    
* **Error Response:**
  * **Code:** 400 <br />
    **Content:** `RES_ERR_MISSING_FIELD`

  OR

  * **Code:** 400 <br />
    **Content:** `RES_ERR_INVALID_FILED`
    
  OR

  * **Code:** 409 <br />
    **Content:** `RES_ERR_USER_EXIST`
    
  OR
  
  * **Code:** 500 <br />
    **Content:** `RES_ERR_TEAM_CREATE`
        
  OR
  
  * **Code:** 500 <br />
    **Content:** `RES_ERR_INTERNAL_SERVER`
    
    
### 3.2 Login
This checks user's credentials (email, password) and generates a `token` which should be used in the api requests for authorization purpose.
`token` has 10 days life time after it is created.
Once `token` is expired, user should login again to get a new valid token.

* **URL**

    /login/

* **Method**
  
    POST
  
* **Data params**
    - email
        
        (required) Email of the user.
    - password
        
        (required) Password of the user.
        
* **Success Response**    
    * **Code:** 200 <br />
    **Content:** Dictionary with `token` and `expires_at` fields.<br />
    
* **Error Response:**
  * **Code:** 400 <br />
    **Content:** `RES_ERR_MISSING_FIELD`

  OR

  * **Code:** 400 <br />
    **Content:** `RES_ERR_INVALID_FILED`
    
  OR

  * **Code:** 400 <br />
    **Content:** `RES_ERR_INVALID_CREDENTIAL`    
    
  OR

  * **Code:** 500 <br />
    **Content:** `RES_ERR_INTERNAL_SERVER`
    
### 3.3 My team
####  3.3.1  View my team
After user logs in he can see his team and player information.
This api returns user's team & player information.

* **URL**

    /my_team/

* **Method**
  
    GET
  
* **Data params**
    - token
        
        (required) user's token which is given after login        
        
* **Success Response**    
    * **Code:** 200 <br />
    **Content:** Dictionary of team data including its members <br />
    
* **Error Response:**
  * **Code:** 401 <br />
    **Content:** `RES_ERR_TOKEN_REQUIRED`

  OR

  * **Code:** 401 <br />
    **Content:** `RES_ERR_INVALID_TOKEN`
    
  OR

  * **Code:** 500 <br />
    **Content:** `RES_ERR_INTERNAL_SERVER`


#### 3.3.2 Update my team
User can update his team's `name`, `country` and member's `first_name`, `last_name` and `country`.

* **URL**

    /my_team/

* **Method**
  
    PUT
  
* **Data params**
    - token
        
        (required) User's token which is given after login
        
    - team_name
        
        (optional) New name of the team
    
    - team_country
        
        (optional) New country name of the team
        
    - member_id
        
        (optional) Member id to be updated
        
    - member_first_name
        
        (optional) New first name of the member
        
    - member_last_name
        
        (optional) New last name of the member
        
    - member_country
        (optional) New country name of the member
        
    ##### Note: At least one of `team_name`, `team_country`, `member_id` should be passed. If `member_id` is passed, at least one of `member_first_name`, `member_last_name`, `member_country` should be passed. <br>
    
    
* **Success Response**    
    * **Code:** 200 <br />
    **Content:** `RES_OK_TEAM_UPDATED`
    
* **Error Response:**
  * **Code:** 401 <br />
    **Content:** `RES_ERR_TOKEN_REQUIRED`

  OR

  * **Code:** 401 <br />
    **Content:** `RES_ERR_INVALID_TOKEN`
    
  OR

  * **Code:** 401 <br />
    **Content:** `RES_ERR_INVALID_PERMISSION`
    
  OR

  * **Code:** 400 <br />
    **Content:** `RES_ERR_MISSING_FIELD`
    
  OR

  * **Code:** 400 <br />
    **Content:** `RES_ERR_INVALID_FILED`    
    
  OR

  * **Code:** 500 <br />
    **Content:** `RES_ERR_INTERNAL_SERVER`
    
    
### 3.4 Market
#### 3.4.1 List all members on the market
User can list all members on the market. They can filter members country name, team name, player name and market price.

* **URL**

    /market/

* **Method**
  
    GET
  
* **Data params**
    - token
        
        (required) User's token which is given after login
        
    - filter_country
        
        (optional) Country name to filter members on the market
    
    - filter_team_name
    
        (optional) Team name to filter members on the market        
        
    - filter_player_name
    
        (optional) Player name to filter members on the market
        
    - filter_value_lte
    
        (optional) `Less than or equal` value to filter members on the market. (If passed, it should be >= 0)
        
     - filter_value_gte
    
        (optional) `Greater than or equal` value to filter members on the market (If passed, it should be >= 0)
        
* **Success Response**    
    * **Code:** 200 <br />
    **Content:** List of dictionary which includes members information (`member_id`, `first_name`, `last_name`, `country`, `team_name`, `price`)on the market.
    
* **Error Response:**
  * **Code:** 401 <br />
    **Content:** `RES_ERR_TOKEN_REQUIRED`

  OR

  * **Code:** 401 <br />
    **Content:** `RES_ERR_INVALID_TOKEN`
    
  OR

  * **Code:** 400 <br />
    **Content:** `RES_ERR_INVALID_FILED`    
    
  OR

  * **Code:** 500 <br />
    **Content:** `RES_ERR_INTERNAL_SERVER`    
    
   
#### 3.4.2 Set a member on the market
User can set his team's member on the market. User should set the askig price when he sets his player on the market and the member should be bought for this price.

* **URL**

    /market/

* **Method**
  
    POST
  
* **Data params**
    - token
        
        (required) User's token which is given after login
    
    - member_id
        
        (required) Member's id to set on the market
        
    - price
        
        (required) Price on the market. (Should be >= 0)                     
        
* **Success Response**    
    * **Code:** 201 <br />
    **Content:** `RES_OK_SET_ON_TRANSFER_LIST`
    
* **Error Response:**
  * **Code:** 401 <br />
    **Content:** `RES_ERR_TOKEN_REQUIRED`

  OR

  * **Code:** 401 <br />
    **Content:** `RES_ERR_INVALID_TOKEN`
    
  OR

  * **Code:** 401 <br />
    **Content:** `RES_ERR_INVALID_PERMISSION`
  
  OR

  * **Code:** 400 <br />
    **Content:** `RES_ERR_MISSING_FIELD`
   
  OR

  * **Code:** 400 <br />
    **Content:** `RES_ERR_INVALID_FILED`    
    
  OR

  * **Code:** 400 <br />
    **Content:** `RES_ERR_ALREADY_ON_MARKET`
    
  OR

  * **Code:** 500 <br />
    **Content:** `RES_ERR_INTERNAL_SERVER`    
    
#### 3.4.3  Buy a member on the market
User can buy members on the market. To buy a member on the market, the user's team's extra money should be greater or equal than the member's market price.
When user is bought, both team's budget are updated, and the user's value is increased by 10-100%.
User can't buy his own member on the market.

* **URL**

    /market/

* **Method**
  
    PUT
  
* **Data params**
    - token
        
        (required) User's token which is given after login
    
    - member_id
        
        (required) Member's id to be bought                     
        
* **Success Response**    
    * **Code:** 200 <br />
    **Content:** `RES_OK_BUY_PLAYER`
    
* **Error Response:**
  * **Code:** 401 <br />
    **Content:** `RES_ERR_TOKEN_REQUIRED`

  OR

  * **Code:** 401 <br />
    **Content:** `RES_ERR_INVALID_TOKEN`
  
  OR

  * **Code:** 401 <br />
    **Content:** `RES_ERR_INVALID_PERMISSION`
    
  OR

  * **Code:** 400 <br />
    **Content:** `RES_ERR_MISSING_FIELD`
   
  OR

  * **Code:** 400 <br />
    **Content:** `RES_ERR_INVALID_FILED`    
    
  OR

  * **Code:** 400 <br />
    **Content:** `RES_ERR_MEMBER_NOT_ON_MARKET`
    
  OR

  * **Code:** 400 <br />
    **Content:** `RES_ERR_NOT_ALLOW_TO_BUY_OWN_PLAYER`
    
  OR

  * **Code:** 400 <br />
    **Content:** `RES_ERR_NOT_ENOUGH_MONEY_TO_BUY`
    
  OR

  * **Code:** 500 <br />
    **Content:** `RES_ERR_INTERNAL_SERVER`  

    
### 3.5 User
##### (for `administrator`), CRUD function for users
#### 3.5.1 User create
Create a user and his team.
The team should be generated by automatically.

* **URL**

    /user/

* **Method**
  
    POST
  
* **Data params**
    - token
        
        (required) Administrator's token which is given after login
            
    - email
        
        (required) New user's email
            
    - password
    
        (required) New user's password
        
* **Success Response**    
    * **Code:** 201 <br />
    **Content:** `RES_OK_USER_CREATED`
    
* **Error Response:**
  * **Code:** 401 <br />
    **Content:** `RES_ERR_TOKEN_REQUIRED`

  OR

  * **Code:** 401 <br />
    **Content:** `RES_ERR_INVALID_TOKEN`
  
  OR

  * **Code:** 401 <br />
    **Content:** `RES_ERR_INVALID_PERMISSION`
    
  OR

  * **Code:** 400 <br />
    **Content:** `RES_ERR_MISSING_FIELD`
   
  OR

  * **Code:** 400 <br />
    **Content:** `RES_ERR_INVALID_FILED`    
    
  OR

  * **Code:** 409 <br />
    **Content:** `RES_ERR_USER_EXIST`
    
  OR

  * **Code:** 500 <br />
    **Content:** `RES_ERR_TEAM_CREATE`
    
  OR

  * **Code:** 500 <br />
    **Content:** `RES_ERR_INTERNAL_SERVER`  
     
     
#### 3.5.2 User list
List all users (`administrators` won't be listed).

* **URL**

    /user/

* **Method**
  
    GET
  
* **Data params**
    - token
        
        (required) Administrator's token which is given after login
        
* **Success Response**
    * **Code:** 200 <br />
    **Content:** List of dictionary of all user's data. (`id`, `email`, `password`)
    
* **Error Response:**
  * **Code:** 401 <br />
    **Content:** `RES_ERR_TOKEN_REQUIRED`

  OR

  * **Code:** 401 <br />
    **Content:** `RES_ERR_INVALID_TOKEN`
  
  OR

  * **Code:** 401 <br />
    **Content:** `RES_ERR_INVALID_PERMISSION`
    
  OR

  * **Code:** 500 <br />
    **Content:** `RES_ERR_INTERNAL_SERVER`  

    
#### 3.5.3 User update
Update user's data. (`password`)

* **URL**

    /user/

* **Method**
  
    PUT
  
* **Data params**
    - token
        
        (required) Administrator's token which is given after login
        
    - email
    
        (required) Email of user to be updated
        
    - password
    
        (required) New password of the user
        
* **Success Response**
    * **Code:** 200 <br />
    **Content:** `RES_OK_USER_UPDATED`
    
* **Error Response:**
  * **Code:** 401 <br />
    **Content:** `RES_ERR_TOKEN_REQUIRED`

  OR

  * **Code:** 401 <br />
    **Content:** `RES_ERR_INVALID_TOKEN`
  
  OR

  * **Code:** 401 <br />
    **Content:** `RES_ERR_INVALID_PERMISSION`
    
  OR

  * **Code:** 400 <br />
    **Content:** `RES_ERR_MISSING_FIELD`
    
  OR

  * **Code:** 400 <br />
    **Content:** `RES_ERR_INVALID_FILED`
    
  OR

  * **Code:** 400 <br />
    **Content:** `RES_ERR_USER_NOT_EXIST`
    
  OR

  * **Code:** 500 <br />
    **Content:** `RES_ERR_INTERNAL_SERVER`


#### 3.5.4 User delete
Delete user. This deletes his team and members as well.

* **URL**

    /user/

* **Method**
  
    DELETE
  
* **Data params**
    - token
        
        (required) Administrator's token which is given after login
        
    - email
    
        (required) Email of user to be deleted
        
* **Success Response**
    * **Code:** 204 <br />
    **Content:** `RES_OK_USER_DELETED`
    
* **Error Response:**
  * **Code:** 401 <br />
    **Content:** `RES_ERR_TOKEN_REQUIRED`

  OR

  * **Code:** 401 <br />
    **Content:** `RES_ERR_INVALID_TOKEN`
  
  OR

  * **Code:** 401 <br />
    **Content:** `RES_ERR_INVALID_PERMISSION`
    
  OR

  * **Code:** 400 <br />
    **Content:** `RES_ERR_MISSING_FIELD`
    
  OR

  * **Code:** 400 <br />
    **Content:** `RES_ERR_INVALID_FILED`
    
  OR

  * **Code:** 400 <br />
    **Content:** `RES_ERR_USER_NOT_EXIST`
    
  OR

  * **Code:** 500 <br />
    **Content:** `RES_ERR_INTERNAL_SERVER`


### 3.6 Team
##### (for `administrator`)
#### 3.6.1 Team create
Create a team and its members.

* **URL**

    /team/

* **Method**
  
    POST
  
* **Data params**
    - token
        
        (required) Administrator's token which is given after login
        
    - name
    
        (optional) Name of the new team. If skipped, it will be generated automatically.
        
    - country
    
        (optional) Country name of the new team. If skipped, it will be generated automatically.
        
    - extra_value
    
        (optional) Extra value of the team to buy new members. If skipped, it will be set to default 5000000.
        (If passed it should be >= 0)
        
* **Success Response**
    * **Code:** 201 <br />
    **Content:** `RES_OK_TEAM_CREATED`  (team id is included in `team_id` field)
    
* **Error Response:**
  * **Code:** 401 <br />
    **Content:** `RES_ERR_TOKEN_REQUIRED`

  OR

  * **Code:** 401 <br />
    **Content:** `RES_ERR_INVALID_TOKEN`
  
  OR

  * **Code:** 401 <br />
    **Content:** `RES_ERR_INVALID_PERMISSION`
    
  OR

  * **Code:** 400 <br />
    **Content:** `RES_ERR_INVALID_FILED`
    
  OR

  * **Code:** 400 <br />
    **Content:** `RES_ERR_TEAM_CREATE`
    
  OR

  * **Code:** 500 <br />
    **Content:** `RES_ERR_INTERNAL_SERVER`


#### 3.6.2 Team list
List all team information including its members.
##### Note: if `owner_id` is `null` this means the team does not have its owner because administrator created it.

* **URL**

    /team/

* **Method**
  
    GET
  
* **Data params**
    - token
        
        (required) Administrator's token which is given after login
        
* **Success Response**
    * **Code:** 200 <br />
    **Content:** List of dictionary which includes team's information
    
* **Error Response:**
  * **Code:** 401 <br />
    **Content:** `RES_ERR_TOKEN_REQUIRED`

  OR

  * **Code:** 401 <br />
    **Content:** `RES_ERR_INVALID_TOKEN`
  
  OR

  * **Code:** 401 <br />
    **Content:** `RES_ERR_INVALID_PERMISSION`
    
  OR

  * **Code:** 500 <br />
    **Content:** `RES_ERR_INTERNAL_SERVER`


#### 3.6.3 Team update
Update team information. (`name`, `country`, `extra_value`)

* **URL**

    /team/

* **Method**
  
    PUT
  
* **Data params**
    - token
        
        (required) Administrator's token which is given after login
        
    - id
    
        (required) Id of the team to be updated
        
    - name
    
        (optional) New name of the team
        
    - country
    
        (optional) New country name of the team        
        
    - extra_value
    
        (optional) New extra value of the team. (if passed it shuld be >=0 )    
    
    ##### Note: At least one of `name`, `country`, `extra_value` should be provided.    
    
        
* **Success Response**
    * **Code:** 200 <br />
    **Content:** `RES_OK_TEAM_UPDATED`
    
* **Error Response:**
  * **Code:** 401 <br />
    **Content:** `RES_ERR_TOKEN_REQUIRED`

  OR

  * **Code:** 401 <br />
    **Content:** `RES_ERR_INVALID_TOKEN`
  
  OR

  * **Code:** 401 <br />
    **Content:** `RES_ERR_INVALID_PERMISSION`
    
  OR

  * **Code:** 400 <br />
    **Content:** `RES_ERR_MISSING_FIELD`
    
  OR

  * **Code:** 400 <br />
    **Content:** `RES_ERR_INVALID_FILED`
    
  OR

  * **Code:** 400 <br />
    **Content:** `RES_ERR_TEAM_NOT_EXIST` 
    
  OR

  * **Code:** 500 <br />
    **Content:** `RES_ERR_INTERNAL_SERVER`

#### 3.6.4 Team delete
Delete team. This deletes the team's members as well.

* **URL**

    /team/

* **Method**
  
    DELETE
  
* **Data params**
    - token
        
        (required) Administrator's token which is given after login
        
    - id
    
        (required) Id of the team to be updated 
    
        
* **Success Response**
    * **Code:** 204 <br />
    **Content:** `RES_OK_TEAM_DELETED`
    
* **Error Response:**
  * **Code:** 401 <br />
    **Content:** `RES_ERR_TOKEN_REQUIRED`

  OR

  * **Code:** 401 <br />
    **Content:** `RES_ERR_INVALID_TOKEN`
  
  OR

  * **Code:** 401 <br />
    **Content:** `RES_ERR_INVALID_PERMISSION`
    
  OR

  * **Code:** 400 <br />
    **Content:** `RES_ERR_MISSING_FIELD`
    
  OR

  * **Code:** 400 <br />
    **Content:** `RES_ERR_INVALID_FILED`
    
  OR

  * **Code:** 400 <br />
    **Content:** `RES_ERR_TEAM_NOT_EXIST` 
    
  OR

  * **Code:** 500 <br />
    **Content:** `RES_ERR_INTERNAL_SERVER`


### 3.7 Member
##### (for `administrator`)
#### 3.7.1 Member create
Create a member and registers to an existing team or set on the market depend on passed fields in the request.

* **URL**

    /member/

* **Method**
  
    POST
  
* **Data params**
    - token
        
        (required) Administrator's token which is given after login
        
    - first_name
        
        (optional) First name of the new member. If skipped, it will be generated automatically.
        
    - last_name
        
        (optional) Last name of the new member. If skipped, it will be generated automatically.
        
    - country
        
        (optional) Country name of the new member. If skipped, it will be generated automatically.
        
    - age
        
        (optional) Age of the new member. If skipped, it will be generated automatically between 18 and 40.
        (If passed it should be between 18 and 40)
        
    - type     
    
        (optional) Type of the new member. If skipped, it will be generated automatically between 0 and 3.
        (If passed it should be between 0 and 3) <br> 0 -> Goal Keeper, 1 -> Defender, 2 -> Midfielder, 3 -> Attacker
        
    - value
    
        (optional) Value of the new member. If skipped, it will be set to 1000000 by default.
        (If passed, it should be >= 0)
        
    - team_id
    
        (optional) If passed, the member will be added to the team.
        
    - market_price
    
        (optional) If passed, the member will be added to the market with the passed price (should be >= 0).
    
* **Success Response**
    * **Code:** 201 <br />
    **Content:** <br />
    `RES_OK_NEW_MEMBER_REGISTERED_TO_TEAM_AND_MARKET`  (if `team_id`, `market_price` is passed) <br/>
    `RES_OK_NEW_MEMBER_REGISTERED_TO_TEAM`  (else if `team_id` is passed) <br/>
    `RES_OK_NEW_MEMBER_REGISTERED_TO_TEAM`  (else if `market_price` is passed) <br/>
    `RES_OK_MEMBER_CREATED`  (else) <br/>    
    
* **Error Response:**
  * **Code:** 401 <br />
    **Content:** `RES_ERR_TOKEN_REQUIRED`

  OR

  * **Code:** 401 <br />
    **Content:** `RES_ERR_INVALID_TOKEN`
  
  OR

  * **Code:** 401 <br />
    **Content:** `RES_ERR_INVALID_PERMISSION`
    
  OR

  * **Code:** 400 <br />
    **Content:** `RES_ERR_INVALID_FILED`
    
  OR

  * **Code:** 400 <br />
    **Content:** `RES_ERR_TEAM_NOT_EXIST` 
    
  OR

  * **Code:** 500 <br />
    **Content:** `RES_ERR_INTERNAL_SERVER`


#### 3.7.2 Member list
List all members.

* **URL**

    /member/

* **Method**
  
    GET
  
* **Data params**
    - token
        
        (required) Administrator's token which is given after login
    
* **Success Response**
    * **Code:** 200 <br />
    **Content:** List of dictionaries which include member's information (`id`, `first_name`, `last_name`, `country`, `age`, `type`, `value`, `team_id`).
    
    ##### Note: Members who are not included in any teams have `team_id` as `null`.
    
* **Error Response:**
  * **Code:** 401 <br />
    **Content:** `RES_ERR_TOKEN_REQUIRED`

  OR

  * **Code:** 401 <br />
    **Content:** `RES_ERR_INVALID_TOKEN`
  
  OR

  * **Code:** 401 <br />
    **Content:** `RES_ERR_INVALID_PERMISSION`
    
  OR

  * **Code:** 500 <br />
    **Content:** `RES_ERR_INTERNAL_SERVER`


#### 3.7.3 Member update
Update member's information.

* **URL**

    /member/

* **Method**
  
    PUT
  
* **Data params**
    - token
        
        (required) Administrator's token which is given after login
        
    - id
        
        (required) Member's id to be updated
        
    - first_name
    
        (optional) New first name of the member
        
    - last_name
    
        (optional) New last name of the member
        
    - country
    
        (optional) New country name of the member
        
    - age
    
        (optional) New age of the member (if passed it should be between 18 and 40)
    
    - type
    
        (optional) New type of the member. (if passed it should be between 0 and 3)
        <br> 0 -> Goal Keeper, 1 -> Defender, 2 -> Midfielder, 3 -> Attacker
        
    - value
        
        (optional) New value of the member. (if passed it should be >= 0)
    
    ##### note: At least one of optional fields should be provided.    
    
* **Success Response**
    * **Code:** 200 <br />
    **Content:** `RES_OK_MEMBER_UPDATED`
    
* **Error Response:**
  * **Code:** 401 <br />
    **Content:** `RES_ERR_TOKEN_REQUIRED`

  OR

  * **Code:** 401 <br />
    **Content:** `RES_ERR_INVALID_TOKEN`
  
  OR

  * **Code:** 401 <br />
    **Content:** `RES_ERR_INVALID_PERMISSION`    
    
  OR

  * **Code:** 400 <br />
    **Content:** `RES_ERR_MISSING_FIELD`
    
  OR

  * **Code:** 400 <br />
    **Content:** `RES_ERR_INVALID_FILED`  
    
  OR

  * **Code:** 400 <br />
    **Content:** `RES_ERR_MEMBER_NOT_EXIST`    
    
  OR

  * **Code:** 500 <br />
    **Content:** `RES_ERR_INTERNAL_SERVER`
    

#### 3.7.4 Member delete
Delete a member

* **URL**

    /member/

* **Method**
  
    DELETE
  
* **Data params**
    - token
        
        (required) Administrator's token which is given after login
        
    - id
        
        (required) Member's id to be deleted
    
* **Success Response**
    * **Code:** 204 <br />
    **Content:** `RES_OK_MEMBER_DELETED`
    
* **Error Response:**
  * **Code:** 401 <br />
    **Content:** `RES_ERR_TOKEN_REQUIRED`

  OR

  * **Code:** 401 <br />
    **Content:** `RES_ERR_INVALID_TOKEN`
  
  OR

  * **Code:** 401 <br />
    **Content:** `RES_ERR_INVALID_PERMISSION`    
    
  OR

  * **Code:** 400 <br />
    **Content:** `RES_ERR_MISSING_FIELD`
    
  OR

  * **Code:** 400 <br />
    **Content:** `RES_ERR_INVALID_FILED`  
    
  OR

  * **Code:** 400 <br />
    **Content:** `RES_ERR_MEMBER_NOT_EXIST`    
    
  OR

  * **Code:** 500 <br />
    **Content:** `RES_ERR_INTERNAL_SERVER`


### 3.8 Add new member to a team
##### (for `administrator`)
Pass `team_id` to member create api (3.7.1) for this purpose.


### 3.9 Add new member on the market
##### (for `administrator`)
Pass `market_price` to member create api (3.7.1) for this purpose.


## 4. Deploy and test
### 4.1 Deploy on development environment
### 4.2 Deploy on production environment
### 4.3 Test
#### 4.3.1 Unit test
#### 4.3.2 E2E test

## 5. Result codes

## 6. Others



