# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s memo.contenttypes -t test_works.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src memo.contenttypes.testing.MEMO_CONTENTTYPES_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/memo/contenttypes/tests/robot/test_works.robot
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

Scenario: As a site administrator I can add a works
  Given a logged-in site administrator
    and an add works form
   When I type 'My works' into the title field
    and I submit the form
   Then a works with the title 'My works' has been created

Scenario: As a site administrator I can view a works
  Given a logged-in site administrator
    and a works 'My works'
   When I go to the works view
   Then I can see the works title 'My works'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add works form
  Go To  ${PLONE_URL}/++add++works

a works 'My works'
  Create content  type=works  id=my-works  title=My works

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the works view
  Go To  ${PLONE_URL}/my-works
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a works with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the works title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
