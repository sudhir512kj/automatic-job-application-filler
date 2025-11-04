import React from 'react';
import { Alert, ListGroup, Badge } from 'react-bootstrap';

const ResultDisplay = ({ result }) => {
  if (!result) return null;

  console.log('Result Display Data:', result);

  return (
    <div>
      {result.success ? (
        <Alert variant="success" className="shadow-sm">
          <Alert.Heading className="h5">
            <i className="bi bi-check-circle-fill me-2"></i>
            Form Submitted Successfully!
          </Alert.Heading>
          <p className="mb-2">
            <i className="bi bi-info-circle me-2"></i>
            Your form was submitted directly via API - no browser redirect needed!
          </p>
          {result.filled_fields && result.filled_fields.length > 0 && (
            <div className="mt-3">
              <p className="mb-2">
                <Badge bg="success" className="me-2">{result.filled_fields.length}</Badge>
                fields filled successfully
              </p>
              <ListGroup variant="flush">
                {result.filled_fields.map((field, index) => (
                  <ListGroup.Item key={index} className="px-0 py-1">
                    <i className="bi bi-check text-success me-2"></i>
                    {field}
                  </ListGroup.Item>
                ))}
              </ListGroup>
            </div>
          )}
          {result.message && (
            <p className="mb-0 mt-2">
              <small className="text-success">
                <i className="bi bi-lightning-fill me-1"></i>
                {result.message}
              </small>
            </p>
          )}
        </Alert>
      ) : (
        <Alert variant="danger" className="shadow-sm">
          <Alert.Heading className="h5">
            <i className="bi bi-exclamation-triangle-fill me-2"></i>
            Error Occurred
          </Alert.Heading>
          {result.error && <p className="mb-0">{result.error}</p>}
        </Alert>
      )}
    </div>
  );
};

export default ResultDisplay;