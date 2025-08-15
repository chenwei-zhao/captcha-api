<template>
  <div class="captcha-container">
    <h1>验证码识别演示</h1>

    <div class="upload-section">
      <div class="upload-box" @dragover.prevent @drop="handleDrop">
        <div v-if="!file" class="upload-placeholder">
          <i class="upload-icon">📁</i>
          <p>拖放图片到此处或点击上传</p>
          <input type="file" ref="fileInput" @change="handleFileChange" accept="image/*">
        </div>
        <div v-else class="file-info">
          <div class="image-wrapper">
            <img ref="imageRef" :src="previewUrl" alt="预览" @load="calculateBox">
            <div v-if="result" class="bounding-box"
                 :style="{
                   left: `${calculatedBox.x}px`,
                   top: `${calculatedBox.y}px`,
                   width: `${calculatedBox.width}px`,
                   height: `${calculatedBox.height}px`,
                   borderColor: getBoxColor(result.confidence)
                 }">
              <div class="box-label" :style="{ backgroundColor: getBoxColor(result.confidence) }">
                {{ (result.confidence * 100).toFixed(1) }}%
              </div>
            </div>
          </div>
          <div class="file-details">
            <p>{{ file.name }}</p>
            <p>{{ (file.size / 1024).toFixed(1) }} KB</p>
          </div>
          <button class="change-btn" @click="resetUpload">更换</button>
        </div>
      </div>

      <div class="options-section">
        <div class="option">
          <label>API版本:</label>
          <select v-model="version">
            <option value="V1">V1</option>
            <option value="V2">V2</option>
          </select>
        </div>

        <div class="option">
          <label>图片类型:</label>
          <select v-model="imageType">
            <option value="background">Background</option>
            <option value="screenshot">Screenshot</option>
          </select>
        </div>
      </div>

      <button class="process-btn" @click="processCaptcha" :disabled="!file || isProcessing">
        <span v-if="isProcessing">识别中...</span>
        <span v-else>识别验证码</span>
      </button>
    </div>

    <div v-if="error" class="error-message">
      <i class="error-icon">⚠️</i> {{ error }}
    </div>

    <div v-if="result" class="results-section">
      <div class="results-header">
        <h2>识别结果</h2>
      </div>
      <div class="result-details">
        <p>置信度: {{ (result.confidence * 100).toFixed(1) }}%</p>
        <p>坐标: 左上角({{ result.box[0] }}, {{ result.box[1] }}) - 右下角({{ result.box[2] }}, {{ result.box[3] }})</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'CaptchaDetector',
  data() {
    return {
      file: null,
      previewUrl: null,
      isProcessing: false,
      error: null,
      result: null,
      calculatedBox: null,
      version: 'V2',
      imageType: 'background'
    };
  },
  methods: {
    handleFileChange(e) {
      this.file = e.target.files[0];
      this.previewUrl = URL.createObjectURL(this.file);
      this.error = null;
      this.result = null;
      this.calculatedBox = null;
    },
    handleDrop(e) {
      e.preventDefault();
      if (e.dataTransfer.files && e.dataTransfer.files[0]) {
        this.file = e.dataTransfer.files[0];
        this.previewUrl = URL.createObjectURL(this.file);
        this.error = null;
        this.result = null;
        this.calculatedBox = null;
      }
    },
    resetUpload() {
      this.file = null;
      this.previewUrl = null;
      this.result = null;
      this.calculatedBox = null;
      this.$refs.fileInput.value = '';
    },
    async processCaptcha() {
      if (!this.file) {
        this.error = '请选择图片文件';
        return;
      }

      this.isProcessing = true;
      this.error = null;
      this.result = null;
      this.calculatedBox = null;

      const formData = new FormData();
      formData.append('file', this.file);
      formData.append('version', this.version);
      formData.append('image_type', this.imageType);

      try {
        const response = await axios.post(
            'http://localhost:8000/captcha',
            formData,
            {
              headers: {
                'Content-Type': 'multipart/form-data'
              }
            }
        );

        this.result = response.data;
        this.calculateBox();
      } catch (err) {
        this.error = `识别失败: ${err.response?.data?.detail || err.message}`;
      } finally {
        this.isProcessing = false;
      }
    },
    calculateBox() {
      if (!this.result || !this.$refs.imageRef) return;

      const imgElement = this.$refs.imageRef;
      const imgWidth = imgElement.naturalWidth;
      const imgHeight = imgElement.naturalHeight;

      const displayWidth = imgElement.offsetWidth;
      const displayHeight = imgElement.offsetHeight;

      const scaleX = displayWidth / imgWidth;
      const scaleY = displayHeight / imgHeight;

      const [x1, y1, x2, y2] = this.result.box;

      this.calculatedBox = {
        x: x1 * scaleX,
        y: y1 * scaleY,
        width: (x2 - x1) * scaleX,
        height: (y2 - y1) * scaleY
      };
    },
    getBoxColor(confidence) {
      if (confidence > 0.9) return '#10B981';  // 绿色
      if (confidence > 0.7) return '#F59E0B';  // 黄色
      return '#EF4444';  // 红色
    }
  }
};
</script>

<style scoped>

.image-wrapper {
  position: relative;
  max-width: 100%;
  margin-bottom: 15px;
}

.bounding-box {
  position: absolute;
  border: 2px solid;
  border-radius: 4px;
}

.box-label {
  position: absolute;
  top: -25px;
  left: -2px;
  padding: 2px 8px;
  border-radius: 4px 4px 0 0;
  font-size: 12px;
  font-weight: 600;
  color: white;
}

.results-section {
  background: white;
  border-radius: 12px;
  padding: 20px;
  margin-top: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.result-details {
  margin-top: 10px;
}

.result-details p {
  margin: 5px 0;
  color: #4A5568;
}


.options-section {
  display: flex;
  gap: 20px;
  margin: 20px 0;
}

.option {
  flex: 1;
}

.option label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #4A5568;
}

.option select {
  width: 100%;
  padding: 10px;
  border: 1px solid #E2E8F0;
  border-radius: 6px;
  background: white;
  font-size: 14px;
}

.captcha-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

h1 {
  text-align: center;
  color: #2D3748;
  margin-bottom: 10px;
}

.subtitle {
  text-align: center;
  color: #718096;
  margin-bottom: 40px;
}

.upload-section {
  background: #F7FAFC;
  border-radius: 12px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.upload-box {
  border: 2px dashed #CBD5E0;
  border-radius: 8px;
  padding: 40px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 20px;
  position: relative;
}

.upload-box:hover {
  border-color: #4299E1;
  background: #EBF8FF;
}

.upload-placeholder {
  color: #718096;
}

.upload-icon {
  font-size: 48px;
  display: block;
  margin-bottom: 15px;
}

input[type="file"] {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
}

.file-info {
  display: flex;
  align-items: center;
  gap: 20px;
}

.thumbnail {
  width: 80px;
  height: 80px;
  border-radius: 8px;
  overflow: hidden;
  background: #EDF2F7;
}

.thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.file-details {
  flex: 1;
  text-align: left;
}

.file-details p {
  margin: 5px 0;
  color: #2D3748;
}

.change-btn {
  background: #EDF2F7;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  color: #2D3748;
  cursor: pointer;
  transition: background 0.3s;
}

.change-btn:hover {
  background: #E2E8F0;
}

.process-btn {
  background: #4299E1;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  width: 100%;
  transition: background 0.3s;
}

.process-btn:hover:not(:disabled) {
  background: #3182CE;
}

.process-btn:disabled {
  background: #CBD5E0;
  cursor: not-allowed;
}

.error-message {
  background: #FED7D7;
  color: #E53E3E;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.results-section {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  padding: 30px;
  margin-top: 30px;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #E2E8F0;
}

.stats {
  display: flex;
  gap: 20px;
  color: #718096;
  font-size: 14px;
}

.image-results {
  margin-bottom: 30px;
}

.image-container {
  background: #F7FAFC;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.image-wrapper {
  position: relative;
  max-width: 100%;
  margin-bottom: 15px;
}

.image-wrapper img {
  max-width: 100%;
  max-height: 500px;
  display: block;
  border-radius: 4px;
}

.bounding-box {
  position: absolute;
  border: 2px solid;
  border-radius: 4px;
  box-sizing: border-box;
}

.box-label {
  position: absolute;
  top: -25px;
  left: -2px;
  padding: 2px 8px;
  border-radius: 4px 4px 0 0;
  font-size: 12px;
  font-weight: 600;
  color: white;
}

.image-caption {
  color: #718096;
  font-size: 14px;
  text-align: center;
}

.results-details h3 {
  margin-top: 30px;
  margin-bottom: 15px;
  color: #2D3748;
}

.results-table {
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  overflow: hidden;
}

.table-header, .table-row {
  display: grid;
  grid-template-columns: 1fr 2fr 2fr 1fr;
  padding: 12px 15px;
  align-items: center;
}

.table-header {
  background: #F7FAFC;
  font-weight: 600;
  color: #2D3748;
}

.table-row {
  border-top: 1px solid #E2E8F0;
}

.table-row:nth-child(even) {
  background: #F7FAFC;
}

.confidence-bar {
  background: #EDF2F7;
  height: 24px;
  border-radius: 4px;
  position: relative;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: #4299E1;
  transition: width 0.5s ease;
}

.confidence-bar span {
  position: absolute;
  top: 50%;
  left: 10px;
  transform: translateY(-50%);
  color: white;
  font-size: 12px;
  font-weight: 600;
  z-index: 1;
}
</style>