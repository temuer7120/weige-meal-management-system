<template>
  <div class="image-ocr">
    <el-upload
      class="upload-demo"
      action="#"
      :auto-upload="false"
      :on-change="handleFileChange"
      :show-file-list="false"
      accept="image/*"
      :multiple="false"
    >
      <el-button type="primary">
        <el-icon><Upload /></el-icon>
        上传图片
      </el-button>
      <el-button type="success" style="margin-left: 10px" @click="takePhoto">
        <el-icon><Camera /></el-icon>
        拍照
      </el-button>
    </el-upload>

    <!-- 图片预览 -->
    <div v-if="imageUrl" class="image-preview">
      <el-image
        :src="imageUrl"
        fit="contain"
        style="width: 400px; height: 300px"
      />
      <div class="image-actions">
        <el-button type="primary" @click="processImage" :loading="processing">
          <el-icon><MagicStick /></el-icon>
          {{ processing ? '识别中...' : '开始识别' }}
        </el-button>
        <el-button @click="clearImage">
          <el-icon><Delete /></el-icon>
          清除
        </el-button>
      </div>
    </div>

    <!-- 识别结果 -->
    <div v-if="ocrResult" class="ocr-result">
      <el-card>
        <template #header>
          <span>识别结果</span>
        </template>
        <el-divider />
        <pre>{{ ocrResult.text }}</pre>
        <el-divider />
        <div class="result-actions">
          <el-button type="primary" @click="autoFillForm">
            <el-icon><Check /></el-icon>
            自动填充表单
          </el-button>
          <el-button @click="copyResult">
            <el-icon><DocumentCopy /></el-icon>
            复制结果
          </el-button>
        </div>
      </el-card>
    </div>

    <!-- 拍照功能 -->
    <input
      ref="fileInput"
      type="file"
      accept="image/*"
      capture="camera"
      style="display: none"
      @change="handlePhotoTaken"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Upload, Camera, MagicStick, Delete, Check, DocumentCopy } from '@element-plus/icons-vue'

// 引入Tesseract.js
import Tesseract from 'tesseract.js'

const imageUrl = ref('')
const processing = ref(false)
const ocrResult = ref(null)
const fileInput = ref(null)

// 定义事件
const emit = defineEmits(['ocr-complete', 'fill-form'])

// 处理文件上传
const handleFileChange = (file) => {
  const reader = new FileReader()
  reader.onload = (e) => {
    imageUrl.value = e.target.result
  }
  reader.readAsDataURL(file.raw)
}

// 拍照功能
const takePhoto = () => {
  if (fileInput.value) {
    fileInput.value.click()
  }
}

// 处理拍照结果
const handlePhotoTaken = (e) => {
  const file = e.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      imageUrl.value = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

// 处理图片
const processImage = async () => {
  if (!imageUrl.value) return
  
  processing.value = true
  
  try {
    // 使用Tesseract.js进行OCR识别
    const result = await Tesseract.recognize(
      imageUrl.value,
      'chi_sim+eng', // 中文+英文
      {
        logger: (m) => console.log(m)
      }
    )
    
    ocrResult.value = result
    emit('ocr-complete', result)
  } catch (error) {
    console.error('OCR处理失败:', error)
  } finally {
    processing.value = false
  }
}

// 清除图片
const clearImage = () => {
  imageUrl.value = ''
  ocrResult.value = null
}

// 自动填充表单
const autoFillForm = () => {
  if (!ocrResult.value) return
  
  // 解析识别结果，提取表单数据
  const formData = parseOcrResult(ocrResult.value.text)
  emit('fill-form', formData)
}

// 复制结果
const copyResult = async () => {
  if (!ocrResult.value) return
  
  try {
    await navigator.clipboard.writeText(ocrResult.value.text)
    alert('复制成功')
  } catch (error) {
    console.error('复制失败:', error)
  }
}

// 解析OCR结果
const parseOcrResult = (text) => {
  const formData = {}
  
  // 示例：解析常见表单字段
  const patterns = {
    name: /姓名[:：]\s*(.+)/,
    phone: /电话[:：]\s*(\d+)/,
    address: /地址[:：]\s*(.+)/,
    price: /价格[:：]\s*(\d+(\.\d+)?)/,
    quantity: /数量[:：]\s*(\d+)/,
    code: /编码[:：]\s*(.+)/,
    date: /日期[:：]\s*(\d{4}-\d{2}-\d{2}|\d{4}\/\d{2}\/\d{2})/
  }
  
  for (const [key, pattern] of Object.entries(patterns)) {
    const match = text.match(pattern)
    if (match) {
      formData[key] = match[1]
    }
  }
  
  return formData
}
</script>

<style scoped>
.image-ocr {
  margin: 20px 0;
}

.image-preview {
  margin: 20px 0;
}

.image-actions {
  margin-top: 10px;
}

.ocr-result {
  margin-top: 20px;
}

.result-actions {
  margin-top: 10px;
}

pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: 'Courier New', Courier, monospace;
  background-color: #f5f7fa;
  padding: 10px;
  border-radius: 4px;
  max-height: 200px;
  overflow-y: auto;
}
</style>
