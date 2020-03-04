# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s memo.contenttypes -t test_work.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src memo.contenttypes.testing.MEMO_CONTENTTYPES_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/memo/contenttypes/tests/robot/test_work.robot
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

Scenario: As a site administrator I can add a Work
  Given a logged-in site administrator
    and an add Work form
   When I type 'My Work' into the title field
    and I submit the form
   Then a Work with the title 'My Work' has been created

Scenario: As a site administrator I can view a Work
  Given a logged-in site administrator
    and a Work 'My Work'
   When I go to the Work view
   Then I can see the Work title 'My Work'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Work form
  Go To  ${PLONE_URL}/++add++Work

a Work 'My Work'
  Create content  type=Work  id=my-work  title=My Work

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Work view
  Go To  ${PLONE_URL}/my-work
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Work with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Work title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
