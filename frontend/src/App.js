import React, { useState } from 'react';
import { TextField, Button, Typography } from '@mui/material';

function App() {
  const [inputText, setInputText] = useState('');
  const [generatedText, setGeneratedText] = useState('');

  const generateText = () => {
    fetch('http://localhost:8000/generate-text', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ text: inputText })
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        setGeneratedText(data.generated_text);
      })
      .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
      });
  };

  const postToLinkedIn = () => {
    fetch('http://localhost:8000/publish-post', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ text: generatedText })
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      console.log('Text posted to LinkedIn successfully.');
    })
    .catch(error => {
      console.error('There was a problem posting to LinkedIn:', error);
    });
  };

  return (
    <div>
      <div>
        <label htmlFor="textInput">Enter Text:</label>
        <TextField
          id="textInput"
          type="text"
          value={inputText}
          onChange={e => setInputText(e.target.value)}
          variant="outlined"
        />
        <Button variant="contained" color="primary" onClick={generateText}>
          Generate
        </Button>
      </div>
      <div>
        <Typography variant="h6" gutterBottom>
          Generated Text:
        </Typography>
        <textarea
          id="generatedText"
          rows="5"
          cols="50"
          readOnly
          value={generatedText}
          style={{ resize: 'none' }}
        />
        <Button variant="contained" color="primary" onClick={postToLinkedIn}>
          Post to LinkedIn
        </Button>
      </div>
    </div>
  );
}

export default App;
