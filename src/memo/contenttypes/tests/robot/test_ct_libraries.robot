# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s memo.contenttypes -t test_libraries.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src memo.contenttypes.testing.MEMO_CONTENTTYPES_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/memo/contenttypes/tests/robot/test_libraries.robot
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

Scenario: As a site administrator I can add a libraries
  Given a logged-in site administrator
    and an add libraries form
   When I type 'My libraries' into the title field
    and I submit the form
   Then a libraries with the title 'My libraries' has been created

Scenario: As a site administrator I can view a libraries
  Given a logged-in site administrator
    and a libraries 'My libraries'
   When I go to the libraries view
   Then I can see the libraries title 'My libraries'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add libraries form
  Go To  ${PLONE_URL}/++add++libraries

a libraries 'My libraries'
  Create content  type=libraries  id=my-libraries  title=My libraries

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the libraries view
  Go To  ${PLONE_URL}/my-libraries
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a libraries with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the libraries title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
