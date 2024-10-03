import React, { Suspense } from 'react';
import ReactDOM from 'react-dom/client';
import '@babel/polyfill';
import App from './app.jsx';
import { BrowserRouter } from 'react-router-dom';
import { Auth0Provider } from '@auth0/auth0-react';
import Central from './contexts/Central';
ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <Suspense>
        <Central>
          <Auth0Provider
            domain="dev-a7ongzyac10pu6qz.us.auth0.com"
            clientId="QpGPEmGwmtWGCzXcWeDyK6DhyRTBdIFm"
            authorizationParams={{
              redirect_uri: 'https://chat-with-vidf.vercel.app/chatbot',
            }}
          >
            <App />
          </Auth0Provider>
        </Central>
      </Suspense>
    </BrowserRouter>
  </React.StrictMode>
);
