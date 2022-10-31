*** Settings ***
Library     SeleniumLibrary
Library    Collections

Test Teardown   Close All Browsers

*** Test Cases ***
Get_removed_spring_properties
    [Documentation]     Get removed sprinmg properties for version 2.7.0
    Open_browser_on_url     https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-2.7.0-Configuration-Changelog
    @{list}             Get_table_column_values     //*[@id="wiki-body"]/div/div[4]/div/table
    Write_list_on_console   @{list}

Get_depraceted_spring_properties
    [Documentation]     Get depraceted sprinmg properties for version 2.7.0
    Open_browser_on_url     https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-2.7.0-Configuration-Changelog
    @{list}             Get_table_column_values     //*[@id="wiki-body"]/div/div[2]/div/table
    Write_list_on_console   @{list}


*** Keywords ***
Open_browser_on_url
    [Documentation]     Opens browser on given url
    [Arguments]         ${url}
    Open Browser	    ${url}	    Chrome
    Maximize Browser Window

Get_table_column_values
    [Documentation]      Get values from given table on page
    [Arguments]          ${table_path}
    @{column_values}     Get WebElements     ${table_path}/tbody/tr/td[1]/p/code
    @{values_list}       Create List
    FOR    ${value}    IN    @{column_values}
        ${text}           Get Text         ${value}
        Append To List     ${values_list}   ${text}
    END
    [Return]    @{values_list}

Write_list_on_console
    [Documentation]     Write list on console output
    [Arguments]         @{list}
    FOR    ${element}    IN    @{list}
        Log To Console    ${element}
    END