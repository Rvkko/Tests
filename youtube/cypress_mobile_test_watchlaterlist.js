describe('test_watchlaterlist', function() {
  before(() => {
    cy.viewport('iphone-13 pro'); // Set the viewport to a mobile device
  });

  it('Login and perform actions on YouTube', () => {
    cy.visit('https://www.youtube.com/');

    cy.get('a[href="https://accounts.google.com/ServiceLogin?service=youtube&uilel=3&passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Den&ec=65620"]').click();

    cy.get('input[type="email"]').type(Cypress.env('email'));
    cy.get('button:contains("Next")').click();

    cy.get('input[type="password"]').type(Cypress.env('password'));
    cy.get('button:contains("Next")').click();

    cy.get('input#search').type('java full course for free');
    cy.get('button#search-icon-legacy').click();

    cy.get('img[src="https://i.ytimg.com/vi/xk4_1vDrzzo/hq720.jpg?sqp=-oaymwEcCNAFEJQDSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLDIGC1UnH_XVz5NaWdKYCpeXLuUYQ"]').click();

    cy.get('button[title="I like this"]').click();
    cy.get('button[title="Save"]').click();
    cy.get('div#checkboxContainer').click();
    cy.get('yt-icon-button#close-button').click();

    cy.get('yt-icon.style-scope.ytd-logo').click();
    cy.get('a[href="/feed/playlists"]').click();
    cy.get('div.yt-thumbnail-view-model__image').click();

    cy.url().should('include', 'https://www.youtube.com/');
  });
});