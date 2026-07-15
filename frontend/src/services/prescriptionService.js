import api from "../api/api";

export const uploadPrescription = async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    const response = await api.post("/ai/test", formData, {
        headers: {
            "Content-Type": "multipart/form-data",
        },
    });

    return response.data;
};