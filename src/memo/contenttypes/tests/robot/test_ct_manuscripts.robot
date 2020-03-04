# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s memo.contenttypes -t test_manuscripts.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src memo.contenttypes.testing.MEMO_CONTENTTYPES_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/memo/contenttypes/tests/robot/test_manuscripts.robot
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

Scenario: As a site administrator I can add a manuscripts
  Given a logged-in site administrator
    and an add manuscripts form
   When I type 'My manuscripts' into the title field
    and I submit the form
   Then a manuscripts with the title 'My manuscripts' has been created

Scenario: As a site administrator I can view a manuscripts
  Given a logged-in site administrator
    and a manuscripts 'My manuscripts'
   When I go to the manuscripts view
   Then I can see the manuscripts title 'My manuscripts'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add manuscripts form
  Go To  ${PLONE_URL}/++add++manuscripts

a manuscripts 'My manuscripts'
  Create content  type=manuscripts  id=my-manuscripts  title=My manuscripts

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the manuscripts view
  Go To  ${PLONE_URL}/my-manuscripts
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a manuscripts with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the manuscripts title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
