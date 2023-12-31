import { toast } from 'react-toastify';

const BASE_CONFIG = {
    position: "bottom-right",
    autoClose: 5000,
    hideProgressBar: false,
    closeOnClick: true,
    pauseOnHover: true,
    draggable: false,
    progress: undefined,
    theme: "dark",
}


export function errorAlert(text) {
    const config = {
        ...BASE_CONFIG
    }
    return toast.error(text, config)
}

export function successAlert(text) {
    const config = {
        ...BASE_CONFIG
    }
    return toast.success(text, config)
}

export function infoAlert(text) {
    const config = {
        ...BASE_CONFIG
    }
    return toast.info(text, config)
}

export function warningAlert(text) {
    const config = {
        ...BASE_CONFIG
    }
    return toast.warning(text, config)
}
