import React, { useState } from 'react';
import styled from 'styled-components';
import { FaPlus } from 'react-icons/fa';

const CenteredContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f0f0;
`;

const SidebarButton = styled.button`
  padding: 12px 24px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
  &:hover {
    background-color: #0056b3;
    transform: translateY(-2px);
  }
`;

const ModalBackground = styled.div`
  display: ${(props) => (props.show ? 'flex' : 'none')};
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  justify-content: center;
  align-items: center;
  z-index: 999;
`;

const ModalContent = styled.div`
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
  width: 400px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  position: relative;
  animation: fadeIn 0.3s ease-out;

  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(-10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
`;

const FileInput = styled.input`
  width: 100%;
  padding: 12px;
  margin: 10px 0;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 16px;
`;

const SubmitButton = styled.button`
  padding: 12px 24px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
  &:hover {
    background-color: #0056b3;
    transform: translateY(-2px);
  }
`;

const CloseButton = styled.button`
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
`;

const ChoiceButton = styled.button`
  padding: 12px 24px;
  margin: 10px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
  &:hover {
    background-color: #0056b3;
    transform: translateY(-2px);
  }
`;

const ButtonWithModal = ({ theme, handleSend }) => {
  const [showModal, setShowModal] = useState(false);
  const [fileType, setFileType] = useState('');
  const [file, setFile] = useState(null);

  const handleOpenModal = () => {
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setFileType('');
    setFile(null);
  };

  const handleChoice = (type) => {
    setFileType(type);
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Logic to handle file submission
    if (file) {
      console.log(`File uploaded for ${fileType}:`, file.name);
      // Handle file upload logic here (e.g., sending it to a server)
      handleSend(`${fileType} file uploaded successfully.`, false);
    }
    handleCloseModal();
  };

  return (
    <CenteredContainer style={{ backgroundColor: theme.sidebarBackground, height: '7rem' }}>
      <SidebarButton
        style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '5px' }}
        onClick={handleOpenModal}
      >
        <FaPlus /> Add PDF/Video
      </SidebarButton>
      <ModalBackground show={showModal} onClick={handleCloseModal}>
        <ModalContent
          style={{ backgroundColor: theme.sidebarBackground }}
          onClick={(e) => e.stopPropagation()}
        >
          <CloseButton onClick={handleCloseModal}>&times;</CloseButton>
          <h2>Select File Type</h2>
          <ChoiceButton onClick={() => handleChoice('PDF')}>PDF</ChoiceButton>
          <ChoiceButton onClick={() => handleChoice('Video')}>Video</ChoiceButton>
          {fileType && (
            <>
              <h3>Upload {fileType}</h3>
              <form onSubmit={handleSubmit}>
                <FileInput
                  type="file"
                  accept={fileType === 'PDF' ? 'application/pdf' : 'video/*'}
                  onChange={handleFileChange}
                  required
                />
                <SubmitButton type="submit">Submit</SubmitButton>
              </form>
            </>
          )}
        </ModalContent>
      </ModalBackground>
    </CenteredContainer>
  );
};

export default ButtonWithModal;
