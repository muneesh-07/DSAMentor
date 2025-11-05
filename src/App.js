// src/App.js - Without Fixed Navbar
import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Box } from '@mui/material';
import DifficultyAnalyzer from './components/DifficultyAnalyzer';
import Navbar from './components/Navbar';

// Create custom theme
const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#5D866C',
      light: '#7ba085',
      dark: '#4a6b57',
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#C2A68C',
      light: '#d4b8a0',
      dark: '#a08973',
      contrastText: '#ffffff',
    },
    background: {
      default: '#F5F5F0',
      paper: '#ffffff',
    },
    text: {
      primary: '#2c3e34',
      secondary: '#5a6b62',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: { fontWeight: 700, fontSize: '2.5rem' },
    h2: { fontWeight: 600, fontSize: '2rem' },
    h3: { fontWeight: 600, fontSize: '1.75rem' },
    h4: { fontWeight: 600, fontSize: '1.5rem' },
    h5: { fontWeight: 600, fontSize: '1.25rem' },
    h6: { fontWeight: 600, fontSize: '1.125rem' },
  },
  shape: {
    borderRadius: 12,
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
          fontWeight: 600,
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 16,
          boxShadow: '0 4px 12px rgba(93, 134, 108, 0.15)',
        },
      },
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Navbar />
        <Box sx={{ 
          minHeight: '100vh',
          backgroundColor: 'background.default'
        }}>
          <DifficultyAnalyzer />
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App;
