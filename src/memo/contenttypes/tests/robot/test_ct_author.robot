# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s memo.contenttypes -t test_author.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src memo.contenttypes.testing.MEMO_CONTENTTYPES_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/memo/contenttypes/tests/robot/test_author.robot
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

Scenario: As a site administrator I can add a Author
  Given a logged-in site administrator
    and an add Author form
   When I type 'My Author' into the title field
    and I submit the form
   Then a Author with the title 'My Author' has been created

Scenario: As a site administrator I can view a Author
  Given a logged-in site administrator
    and a Author 'My Author'
   When I go to the Author view
   Then I can see the Author title 'My Author'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Author form
  Go To  ${PLONE_URL}/++add++Author

a Author 'My Author'
  Create content  type=Author  id=my-author  title=My Author

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Author view
  Go To  ${PLONE_URL}/my-author
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Author with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Author title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
