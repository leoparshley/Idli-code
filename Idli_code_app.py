import React, { useState } from 'react';

const wordToBinary = {
  Idli: '00',
  Dosa: '01',
  Sambar: '10',
  Chutney: '11',
};

const binaryToWord = {
  '00': 'Idli',
  '01': 'Dosa',
  '10': 'Sambar',
  '11': 'Chutney',
};

export default function IdliDecoder() {
  const [encodedText, setEncodedText] = useState('');
  const [decodedText, setDecodedText] = useState('');
  const [errorReport, setErrorReport] = useState('');

  const decodeText = () => {
    const words = encodedText
      .trim()
      .replace(/\s+/g, ' ')
      .split(' ');

    let errorAt = null;
    let binaryStr = '';
    let cleanWords = [];

    for (let i = 0; i < words.length; i++) {
      const word = words[i];
      if (!wordToBinary[word]) {
        errorAt = `Invalid word "${word}" at position ${i + 1}`;
        break;
      }
      cleanWords.push(word);
      binaryStr += wordToBinary[word];
    }

    if (errorAt) {
      setDecodedText('');
      setErrorReport(errorAt);
      return;
    }

    const chars = [];
    for (let i = 0; i < binaryStr.length; i += 8) {
      const byte = binaryStr.slice(i, i + 8);
      const charCode = parseInt(byte, 2);
      chars.push(String.fromCharCode(charCode));
    }

    setDecodedText(chars.join(''));
    setErrorReport('');
  };

  return (
    <div className="p-4 space-y-4 max-w-xl mx-auto">
      <textarea
        className="w-full p-2 border rounded"
        rows={6}
        placeholder="Paste Idli-Dosa-Sambar-Chutney encoded message here..."
        value={encodedText}
        onChange={(e) => setEncodedText(e.target.value)}
      />

      <button
        onClick={decodeText}
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
      >
        Decrypt
      </button>

      {errorReport && (
        <div className="text-red-500 font-mono mt-2">Error: {errorReport}</div>
      )}

      {decodedText && (
        <div className="bg-gray-100 p-3 rounded font-mono mt-2">
          {decodedText}
        </div>
      )}
    </div>
  );
}