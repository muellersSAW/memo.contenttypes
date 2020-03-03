# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s memo.contenttypes -t test_language.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src memo.contenttypes.testing.MEMO_CONTENTTYPES_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/memo/contenttypes/tests/robot/test_language.robot
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

Scenario: As a site administrator I can add a Language
  Given a logged-in site administrator
    and an add Language form
   When I type 'My Language' into the title field
    and I submit the form
   Then a Language with the title 'My Language' has been created

Scenario: As a site administrator I can view a Language
  Given a logged-in site administrator
    and a Language 'My Language'
   When I go to the Language view
   Then I can see the Language title 'My Language'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Language form
  Go To  ${PLONE_URL}/++add++Language

a Language 'My Language'
  Create content  type=Language  id=my-language  title=My Language

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Language view
  Go To  ${PLONE_URL}/my-language
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Language with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Language title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
