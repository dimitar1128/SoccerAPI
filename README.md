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
##### Note: This guide is for Ubuntu (18.04 | 20.04) machines. 
- Install `Python (>=3.8)` and `pip3` 
Ubuntu (>=18.04) has `Python` installed already.
Install `pip3` with the following command. <br>
`sudo apt update` <br>
`sudo apt install python3-pip -y` 
- Install dependencies, mysql-server, mysql-client. <br>
`sudo apt install build-essential mysql-server -y` <br>
`sudo apt install libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev -y` <br>
`sudo apt-get install libmysqlclient-dev -y`
- Clone the project as `ToptalSoccer`.
- In the project base folder run below command to install requirements. <br>
`pip3 install -r requirements.txt`
- Create a database named `soccer`.
- Configure database connection information in `ToptalSoccer/settings.py`.
    ```text
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'soccer',
            'HOST': 'localhost',
            'USER': 'root',
            'PASSWORD': '',
            'PORT': '3306',
        }
    }
    ```
    Mysql uses `root` for default username and there is no password by default.
    So if you didn't change this in MySQL you are not required to update database connection in `settings.py`.
- Migrate database.
`python3 manage.py migrate` <br>
This command should generate necessary tables automatically in the database `soccer` that you made.
- Create administrator.
`python3 manage.py createsuperuser`
Then enter `email` and `username` (`username` should be the same with `email`), and its password.
- Run the server. <br>
`python3 manage.py runserver 127.0.0.1:8000` <br>
This runs the server on port 8000. You can change the port if you want. <br>
You would see the below log if the server runs successfully.
```text
System check identified 1 issue (0 silenced).
January 23, 2021 - 18:55:55
Django version 3.0.2, using settings 'ToptalSoccer.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```
<h5>Note</h5>
Use `python` and `pip` on windows machine.

### 4.2 Deploy on production environment
#### 4.2.1 Install dependencies ###
- Prepare Ubuntu (18.04 | 20.04) system.
- Install apache & wsgi module for apache <br>
`sudo apt-get update -y` <br>
`sudo apt install apache2 libapache2-mod-wsgi-py3 -y`
- Enable module alias, ssl, rewrite <br>
`sudo a2enmod alias ssl rewrite`
- Restart apache <br>
`sudo service apache2 restart`
- Install dependencies, mysql-server, mysql-client. <br>
`sudo apt install python3-pip build-essential mysql-server -y` <br>
`sudo apt install libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev -y` <br>
`sudo apt-get install libmysqlclient-dev -y`

<h5>Note</h5> Python3 is installed on most of Ubuntu vms that are provisioned by cloud provider such as AWS and Vultr.
Check the python version.
`python3 --version`

#### 4.2.2 Configure mysql ###
- Enter to mysql cli. <br>
`mysql`
- Create user and grant permission. <br>
`CREATE USER 'admin'@'%' IDENTIFIED BY 'password';` <br>
`GRANT ALL PRIVILEGES ON * . * TO 'admin'@'%';` <br>
`ALTER USER 'admin'@'%' IDENTIFIED WITH mysql_native_password BY 'password';`
- Create database named `soccer` and exit.<br>
`CREATE DATABASE soccer;` <br>
`exit;`
- Update bind address of mysql server to 0.0.0.0 <br>
Open /etc/mysql/mysql.conf.d/mysqld.cnf  and update bind-address to 0.0.0.0
- Restart mysql service. <br>
`systemctl restart mysql`

#### 4.2.3 Clone repository and install dependency packages ###
- Clone the project as `ToptalSoccer` in `/mnt/` directory.
- Grant permission to the project folder and install dependencies. <br>
`cd /mnt/ToptalSoccer` <br>
`chmod 777 -R ./` <br>
`pip3 install -r requirements.txt` <br>

#### 4.2.4 Update settings and migrate database ###
- Replace `settings.py` with `settings_prod.py`. <br>
`cd /mnt/ToptalSoccer` <br>
`mv ToptalSoccer/settings_prod.py ToptalSoccer/settings.py`
- Update database connection information in `ToptalSoccer/settings.py`
  ```text
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'soccer',
            'HOST': '<host ip>',
            'USER': 'admin',
            'PASSWORD': 'password',
            'PORT': '3306',
        }
    }
    ```
- Migrate database
`python3 manage.py migrate`
- Create administrator.
`python3 manage.py createsuperuser`
Then enter `email` and `username` (`username` should be the same with `email`), and its password.

#### 4.2.5 Configure appache ###
- Open apache configuration. <br>
`vim /etc/apache2/sites-available/000-default.conf`
- Add the following to the file of <VirtualHost> tag.
```text
ServerName <host ip>
ServerAlias <host ip>

DocumentRoot /mnt/ToptalSoccer

<Directory "/mnt/ToptalSoccer">
	Require all granted
</Directory>

<Directory /mnt/ToptalSoccer/ToptalSoccer>
	<Files wsgi.py>
		Require all granted
	</Files>
</Directory>

WSGIDaemonProcess ToptalSoccer python-path=/mnt/ToptalSoccer/:/usr/local/lib/python3.8/dist-packages
WSGIProcessGroup ToptalSoccer
WSGIApplicationGroup %{GLOBAL}
WSGIScriptAlias / /mnt/ToptalSoccer/ToptalSoccer/wsgi.py
``` 
- Check configuration with command and then restart apache service. <br>
`sudo apachectl configtest` <br>
`sudo systemctl restart apache2`

<h5>Make sure to open 80 and 3306 ports to outside in the cloud provider.</h5>

### 4.3 Test
Test is implemented by using DRF unit test module.
#### 4.3.1 Unit test
`python3 manage.py test api.s_auth.tests.AuthenticateAPITestCase.test_SignupLogin` <br>
`python3 manage.py test api.team.tests.MyTeamApiTestCase.testGetAndUpdateMyteam` <br>
`python3 manage.py test api.team.tests.MyTeamApiTestCase.testGetAndUpdateMyteam` <br>
`python3 manage.py test api.market.tests.MarketApiTestCase.testSetPlayerOnMarketAndList` <br>
`python3 manage.py test api.market.tests.MarketApiTestCase.testBuyMemberOnMarket` <br>

`python3 manage.py test api.user.tests.UserTestCase.testUserCRUD` <br>
`python3 manage.py test api.team.tests.TeamTestCase.testTeamCRUD` <br>
`python3 manage.py test api.member.tests.MemberTestCase.test_MemberCRUD` <br>
`python3 manage.py test api.member.tests.MemberTestCase.testNewMemberToTeam` <br>
`python3 manage.py test api.member.tests.MemberTestCase.testNewMemberToMarket` <br>

#### 4.3.2 E2E test
`python3 manage.py test api.e2e.tests.E2ETest.test_e2e`

## 5. Result codes
- RES_OK_USER_CREATED
    * **code:** 1001
    * **message:** User has been created
- RES_OK_USER_UPDATED
    * **code:** 1002
    * **message:** User has been updated
- RES_OK_USER_DELETED
    * **code:** 1003
    * **message:** User has been deleted
- RES_OK_TEAM_CREATED
    * **code:** 1004
    * **message:** Team has been created
- RES_OK_TEAM_UPDATED
    * **code:** 1005 
    * **message:** Team has been updated 
- RES_OK_TEAM_DELETED
    * **code:** 1006
    * **message:** Team has been deleted
- RES_OK_MEMBER_CREATED
    * **code:** 1007
    * **message:** Member has been created
- RES_OK_MEMBER_UPDATED
    * **code:** 1008
    * **message:** Member has been updated
- RES_OK_MEMBER_DELETED
    * **code:** 1009
    * **message:** Member has been deleted
- RES_OK_NEW_MEMBER_REGISTERED_TO_TEAM
    * **code:** 1010
    * **message:** Member has been created and registered to the team
- RES_OK_NEW_MEMBER_REGISTERED_TO_MARKET
    * **code:** 1011
    * **message:** Member has been created and registered and added to the market
- RES_OK_NEW_MEMBER_REGISTERED_TO_TEAM_AND_MARKET
    * **code:** 1012
    * **message:** Member has been created and registered to the team, and added to the market
- RES_OK_SET_ON_TRANSFER_LIST
    * **code:** 1013
    * **message:** Player has been set on the transfer list
- RES_OK_BUY_PLAYER
    * **code:** 1014
    * **message:** You have bought the player
<br><br/>
- RES_ERR_MISSING_FIELD
    * **code:** 8001
    * **message:** One or more fields are missing in the request
- RES_ERR_INVALID_FILED
    * **code:** 8002
    * **message:** One or more fields in the request are invalid
<br><br/>
- RES_ERR_USER_EXIST
    * **code:** 8101
    * **message:** The email is already registered
- RES_ERR_USER_NOT_EXIST
    * **code:** 8102
    * **message:** The email is not registered yet
- RES_ERR_TEAM_NOT_EXIST
    * **code:** 8103
    * **message:** The team does not exist
- RES_ERR_MEMBER_NOT_EXIST
    * **code:** 8104
    * **message:** The member does not exist
- RES_ERR_INVALID_CREDENTIAL
    * **code:** 8105
    * **message:** Email or password is not correct
- RES_ERR_ALREADY_ON_MARKET
    * **code:** 8106
    * **message:** The member is already on the transfer list
- RES_ERR_MEMBER_NOT_ON_MARKET
    * **code:** 8107
    * **message:** The member is not on the transfer list
- RES_ERR_NOT_ALLOW_TO_BUY_OWN_PLAYER
    * **code:** 8108
    * **message:** You are not allowed to buy your own player
- RES_ERR_NOT_ENOUGH_MONEY_TO_BUY
    * **code:** 8109
    * **message:** Your team does not have enough money to buy the player
<br><br/>
- RES_ERR_TOKEN_REQUIRED
    * **code:** 8901
    * **message:** Token is required to call api
- RES_ERR_INVALID_TOKEN
    * **code:** 8902
    * **message:** Token is invalid. Please try to login again to get a new valid token
- RES_ERR_INVALID_PERMISSION
    * **code:** 8903
    * **message:** You are not allowed to do this action
<br><br/>
- RES_ERR_INTERNAL_SERVER
    * **code:** 9001
    * **message:** Internal server error
- RES_ERR_TEAM_CREATE
    * **code:** 9002
    * **message:** Server error during team creation
    
## 6. Others
- The api server is deployed in development mode on http://100.27.0.226:7777/ <br>
- All test can be done with postman.
- In the project root directory, there is postman_collection.json file which is for testing the api.
- Test administrator account is `admin@soccer.com` and password is `dimitarsoccer1128`.
- To test administrator role apis, please call `login` api with the above credentials.
It will give you `token` which should be used to call any other administrator apis.
- All the `tokens` in the postman collection should not work so please change it with the one you get after you call the `login` api.


