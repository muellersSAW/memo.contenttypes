# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s memo.contenttypes -t test_m_type.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src memo.contenttypes.testing.MEMO_CONTENTTYPES_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/memo/contenttypes/tests/robot/test_m_type.robot
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

Scenario: As a site administrator I can add a MType
  Given a logged-in site administrator
    and an add MType form
   When I type 'My MType' into the title field
    and I submit the form
   Then a MType with the title 'My MType' has been created

Scenario: As a site administrator I can view a MType
  Given a logged-in site administrator
    and a MType 'My MType'
   When I go to the MType view
   Then I can see the MType title 'My MType'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add MType form
  Go To  ${PLONE_URL}/++add++MType

a MType 'My MType'
  Create content  type=MType  id=my-m_type  title=My MType

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the MType view
  Go To  ${PLONE_URL}/my-m_type
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a MType with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the MType title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
