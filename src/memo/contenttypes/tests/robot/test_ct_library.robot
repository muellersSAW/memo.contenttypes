# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s memo.contenttypes -t test_library.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src memo.contenttypes.testing.MEMO_CONTENTTYPES_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/memo/contenttypes/tests/robot/test_library.robot
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

Scenario: As a site administrator I can add a library
  Given a logged-in site administrator
    and an add library form
   When I type 'My library' into the title field
    and I submit the form
   Then a library with the title 'My library' has been created

Scenario: As a site administrator I can view a library
  Given a logged-in site administrator
    and a library 'My library'
   When I go to the library view
   Then I can see the library title 'My library'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add library form
  Go To  ${PLONE_URL}/++add++library

a library 'My library'
  Create content  type=library  id=my-library  title=My library

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the library view
  Go To  ${PLONE_URL}/my-library
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a library with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the library title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
