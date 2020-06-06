/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

// https://fsnd-nikolai.eu.auth0.com/authorize?audience=coffeeshop&response_type=token&client_id=TqIHsl2HnAEuuZxv9HFXghjP4Hfj5D2F&redirect_uri=http://localhost:8080/login-results

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'fsnd-nikolai.eu', // the auth0 domain prefix
    audience: 'coffeeshop', // the audience set for the auth0 app
    clientId: 'TqIHsl2HnAEuuZxv9HFXghjP4Hfj5D2F', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};


