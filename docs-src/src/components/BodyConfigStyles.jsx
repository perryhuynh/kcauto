export const styles = theme => ({
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
  helperText: {
    fontFamily: 'Roboto, sans-serif',
    fontSize: '0.75rem',
    marginTop: 8,
    lineHeight: '1em',
    color: 'rgba(0, 0, 0, 0.54)',
  },
  clearFormIcon: {
    position: 'absolute',
    bottom: 5,
    right: 2,
    border: 0,
    background: 'none',
    fontFamily: 'Roboto, sans-serif',
    fontSize: 16,
    outline: 'none',
    cursor: 'pointer',
  },
  clearFormIconIntInput: {
    bottom: 13,
    right: 14,
  },
  flexReset: {
    display: 'flex',
  },
  saveButton: {
    marginLeft: 10,
  },
  modal: {
    position: 'absolute',
    width: theme.spacing.unit * 80,
    padding: theme.spacing.unit * 4,
    backgroundColor: theme.palette.background.paper,
    boxShadow: theme.shadows[5],
  },
})
