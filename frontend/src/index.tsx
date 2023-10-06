import * as React from 'react';
import * as ReactDOM from 'react-dom/client';
import CssBaseline from '@mui/material/CssBaseline';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import App from './App';

const rootElement = document.getElementById('root');
const root = ReactDOM.createRoot(rootElement!);

const themeLight = createTheme({
    palette: {
        background: {
            default: "#F0F0F0"
        }
    }
});

root.render(
    <ThemeProvider theme={themeLight}>
        {/* CssBaseline kickstart an elegant, consistent, and simple baseline to build upon. */}
        <CssBaseline/>
        <App/>
    </ThemeProvider>,
);
