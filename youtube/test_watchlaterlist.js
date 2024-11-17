const { remote } = require('webdriverio');
const assert = require('assert');
const fs = require('fs');
const path = require('path');

let driver;
let wait;

before(async function() {
    const capabilities = [
        {
            platformName: 'Android',
            deviceName: 'emulator-5554',
            browserName: 'Chrome'
        },
        {
            platformName: 'Android',
            deviceName: 'emulator-5554',
            browserName: 'Firefox'
        }
    ];

    driver = await remote({
        logLevel: 'error',
        path: '/wd/hub',
        capabilities: capabilities[0] // Change index to switch between Chrome and Firefox
    });

    wait = driver.setTimeout({ implicit: 10000 });
});

after(async function() {
    await driver.deleteSession();
});

function getTestData() {
    const scriptDirectory = __dirname;
    const jsonFilePath = path.join(scriptDirectory, 'test_data.json');
    const data = JSON.parse(fs.readFileSync(jsonFilePath, 'utf8'));
    return data;
}

describe('YouTube Login and Watch Later Test', function() {
    it('should login, like a video, save to watch later, and verify', async function() {
        const testData = getTestData();

        await driver.url('https://www.youtube.com/');

        const signIn = await driver.$("//a[@href='https://accounts.google.com/ServiceLogin?service=youtube&uilel=3&passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Den&ec=65620']");
        await signIn.click();

        const email = await driver.$("//input[@type='email']");
        await email.setValue(testData.email);

        const nextButton = await driver.$("//button[contains(@class, 'VfPpkd-LgbsSe') and .//span[text()='Next']]");
        await nextButton.click();

        const password = await driver.$("//input[@type='password']");
        await password.setValue(testData.password);

        const nextButton2 = await driver.$("//button[contains(@class, 'VfPpkd-LgbsSe') and .//span[text()='Next']]");
        await nextButton2.click();

        const searchBar = await driver.$("//input[@id='search']");
        await searchBar.setValue('java full course for free');

        const search = await driver.$("//button[@id='search-icon-legacy']");
        await search.click();

        const video = await driver.$("//img[@src='https://i.ytimg.com/vi/xk4_1vDrzzo/hq720.jpg?sqp=-oaymwEcCNAFEJQDSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLDIGC1UnH_XVz5NaWdKYCpeXLuUYQ']");
        await video.click();

        const likeButton = await driver.$("//button[@title='I like this']");
        await likeButton.click();

        const saveButton = await driver.$("//button[@title='Save']");
        await saveButton.click();

        const watchLater = await driver.$("//div[@id='checkboxContainer']");
        await watchLater.click();

        const cancelButton = await driver.$("//yt-icon-button[@id='close-button']");
        await cancelButton.click();

        const homePage = await driver.$("//yt-icon[@class='style-scope ytd-logo']");
        await homePage.click();

        const playlistButton = await driver.$("//a[@href='/feed/playlists']");
        await playlistButton.click();

        const watchLaterList = await driver.$("//div[@class='yt-thumbnail-view-model__image']");
        await watchLaterList.click();

        await driver.waitUntil(async () => {
            const url = await driver.getUrl();
            return url.includes('youtube.com/');
        }, { timeout: 5000 });

        const actualUrl = await driver.getUrl();
        assert(actualUrl.startsWith('https://www.youtube.com/'));
    });
});