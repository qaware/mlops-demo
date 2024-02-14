import { createTheme } from '@mui/material/styles';
import { red } from '@mui/material/colors';

// A custom theme for this app
const theme = createTheme({
  typography: {
    fontFamily: 'SpartanMB-Bold, Arial',
    subtitle1: {
      fontFamily: 'SpartanMB-SemiBold, Arial',
    },
    body1: {
      fontFamily: 'SpartanMB-Regular, Arial',
    },
  },
  palette: {
    primary: {
      main: '#17428b',
    },
    secondary: {
      main: '#009ee3',
    },
    error: {
      main: red.A400,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        contained: {
          background: '#009ee3'
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          background: 'linear-gradient(to bottom, #17428b 0%, #009ee3 90%)',
        },
      },
    },
  },
});

export default theme;
