export const styles = () => ({
  dropzoneOverlay: {
    position: 'fixed',
    top: 0,
    left: 0,
    display: 'flex',
    width: '100%',
    height: '100%',
    justifyContent: 'center',
    alignItems: 'center',
    fontFamily: 'Roboto, sans-serif',
    fontSize: 24,
    fontWeight: 'bold',
    background: 'rgba(255,255,255,0.8)',
    zIndex: 9,
  },
  paper: {
    marginTop: 10,
    padding: 20,
  },
  pre: {
    padding: 20,
    fontFamily: '"Source Code Pro", monospace',
    fontSize: 12,
    overflowX: 'auto',
  },
  formGrid: {
    padding: 8,
    paddingTop: 0,
    paddingBottom: 0,
  },
  formGridButton: {
    padding: 0,
    paddingTop: 14,
    textAlign: 'center',
  },
  formControl: {
    marginTop: 0,
  },
  switch: {
    zIndex: 0,
  },
  reactSelectLabel: {
    transform: 'translate(0, -15px) scale(0.75)',
    minWidth: '150%',
  },
  reactSelect: {
    fontFamily: 'Roboto, sans-serif',
  },
  reactSelectHalfWidth: {
    width: '50%',
    fontFamily: 'Roboto, sans-serif',
  },
  flexReset: {
    display: 'flex',
  },
  saveButton: {
    marginLeft: 10,
  },
})
