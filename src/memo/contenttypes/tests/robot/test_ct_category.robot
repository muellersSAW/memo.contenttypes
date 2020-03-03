# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s memo.contenttypes -t test_category.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src memo.contenttypes.testing.MEMO_CONTENTTYPES_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/memo/contenttypes/tests/robot/test_category.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Category
  Given a logged-in site administrator
    and an add Category form
   When I type 'My Category' into the title field
    and I submit the form
   Then a Category with the title 'My Category' has been created

Scenario: As a site administrator I can view a Category
  Given a logged-in site administrator
    and a Category 'My Category'
   When I go to the Category view
   Then I can see the Category title 'My Category'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Category form
  Go To  ${PLONE_URL}/++add++Category

a Category 'My Category'
  Create content  type=Category  id=my-category  title=My Category

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Category view
  Go To  ${PLONE_URL}/my-category
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Category with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Category title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
