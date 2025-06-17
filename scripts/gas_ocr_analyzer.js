/**
 * AUTOCREATE株式会社 - GAS OCR画像解析システム
 * AI社長×無職CTO体制による画像認識自動化
 */

/**
 * スクリーンショット画像をOCRで解析
 * @param {string} imageFileId - Google Driveの画像ファイルID
 * @return {Object} OCR解析結果
 */
function analyzeScreenshot(imageFileId) {
  try {
    // 画像ファイルを取得
    const imageFile = DriveApp.getFileById(imageFileId);
    const blob = imageFile.getBlob();
    
    // Google DocsでOCR実行
    const resource = {
      title: `OCR_${imageFile.getName()}_${new Date().getTime()}`,
      parents: [{id: getOcrFolderId()}]
    };
    
    const ocrFile = Drive.Files.insert(resource, blob, {
      convert: true,
      ocr: true
    });
    
    // OCR結果を取得
    const doc = DocumentApp.openById(ocrFile.id);
    const ocrText = doc.getBody().getText();
    
    // 解析結果を構造化
    const analysis = {
      timestamp: new Date().toISOString(),
      fileName: imageFile.getName(),
      ocrText: ocrText,
      analysis: analyzeScreenContent(ocrText),
      confidence: calculateConfidence(ocrText)
    };
    
    // 結果をスプレッドシートに保存
    saveAnalysisResult(analysis);
    
    // 一時的なOCRファイルを削除
    DriveApp.getFileById(ocrFile.id).setTrashed(true);
    
    return analysis;
    
  } catch (error) {
    console.error('OCR解析エラー:', error);
    return {
      error: error.toString(),
      timestamp: new Date().toISOString()
    };
  }
}

/**
 * 画面内容を分析（kinkaimasu.jp専用）
 * @param {string} ocrText - OCRで抽出されたテキスト
 * @return {Object} 分析結果
 */
function analyzeScreenContent(ocrText) {
  const analysis = {
    isLoginPage: ocrText.includes('ログイン') || ocrText.includes('Login'),
    hasForm: ocrText.includes('入力') || ocrText.includes('送信'),
    hasPrice: /\d+円/.test(ocrText) || /¥\d+/.test(ocrText),
    hasButton: ocrText.includes('ボタン') || ocrText.includes('クリック'),
    hasError: ocrText.includes('エラー') || ocrText.includes('Error'),
    detectedElements: extractScreenElements(ocrText)
  };
  
  return analysis;
}

/**
 * 画面要素を抽出
 * @param {string} text - OCRテキスト
 * @return {Array} 検出された要素リスト
 */
function extractScreenElements(text) {
  const elements = [];
  
  // ボタン要素の検出
  const buttonMatches = text.match(/[\w\s]+ボタン|[\w\s]+Button/g);
  if (buttonMatches) {
    elements.push(...buttonMatches.map(btn => ({type: 'button', text: btn})));
  }
  
  // フォーム要素の検出
  const formMatches = text.match(/[\w\s]+入力|[\w\s]+Input/g);
  if (formMatches) {
    elements.push(...formMatches.map(form => ({type: 'input', text: form})));
  }
  
  // 価格情報の検出
  const priceMatches = text.match(/\d+[円¥]/g);
  if (priceMatches) {
    elements.push(...priceMatches.map(price => ({type: 'price', text: price})));
  }
  
  return elements;
}

/**
 * OCR信頼度を計算
 * @param {string} ocrText - OCRテキスト
 * @return {number} 信頼度スコア（0-100）
 */
function calculateConfidence(ocrText) {
  let score = 0;
  
  // 日本語文字の存在
  if (/[ひらがなカタカナ漢字]/.test(ocrText)) score += 30;
  
  // 英数字の存在
  if (/[a-zA-Z0-9]/.test(ocrText)) score += 20;
  
  // 構造化されたテキスト
  if (ocrText.includes('\n')) score += 20;
  
  // 特定キーワードの存在
  if (ocrText.includes('金買取') || ocrText.includes('kinkaimasu')) score += 30;
  
  return Math.min(score, 100);
}

/**
 * 解析結果をスプレッドシートに保存
 * @param {Object} analysis - 解析結果
 */
function saveAnalysisResult(analysis) {
  const sheet = getAnalysisSheet();
  
  sheet.appendRow([
    analysis.timestamp,
    analysis.fileName,
    analysis.ocrText.substring(0, 500), // 最初の500文字
    JSON.stringify(analysis.analysis),
    analysis.confidence,
    analysis.error || ''
  ]);
}

/**
 * OCR用フォルダIDを取得
 * @return {string} フォルダID
 */
function getOcrFolderId() {
  const folderName = 'AUTOCREATE_OCR_Analysis';
  const folders = DriveApp.getFoldersByName(folderName);
  
  if (folders.hasNext()) {
    return folders.next().getId();
  } else {
    const newFolder = DriveApp.createFolder(folderName);
    return newFolder.getId();
  }
}

/**
 * 解析結果スプレッドシートを取得
 * @return {Sheet} スプレッドシート
 */
function getAnalysisSheet() {
  const ssName = 'AUTOCREATE_Screenshot_Analysis';
  let ss;
  
  try {
    ss = SpreadsheetApp.openByName(ssName);
  } catch (e) {
    ss = SpreadsheetApp.create(ssName);
    const sheet = ss.getActiveSheet();
    sheet.getRange(1, 1, 1, 6).setValues([[
      'Timestamp', 'FileName', 'OCR_Text', 'Analysis', 'Confidence', 'Error'
    ]]);
  }
  
  return ss.getActiveSheet();
}

/**
 * 画像ファイルをアップロードしてOCR実行
 * @param {Blob} imageBlob - 画像データ
 * @param {string} fileName - ファイル名
 * @return {Object} OCR結果
 */
function uploadAndAnalyze(imageBlob, fileName) {
  // Google Driveに画像をアップロード
  const folder = DriveApp.getFolderById(getOcrFolderId());
  const file = folder.createFile(imageBlob.setName(fileName));
  
  // OCR解析実行
  const result = analyzeScreenshot(file.getId());
  
  // 元画像ファイルを削除（必要に応じて）
  // file.setTrashed(true);
  
  return result;
}

/**
 * kinkaimasu.jp専用解析
 * @param {string} imageFileId - 画像ファイルID
 * @return {Object} kinkaimasu.jp解析結果
 */
function analyzeKinkamassu(imageFileId) {
  const baseAnalysis = analyzeScreenshot(imageFileId);
  
  // kinkaimasu.jp特有の要素を検出
  const kinkamasuAnalysis = {
    ...baseAnalysis,
    isKinkamasuSite: baseAnalysis.ocrText.includes('kinkaimasu') || 
                     baseAnalysis.ocrText.includes('金買取'),
    hasGoldPrices: /金価格|ゴールド|1g|相場/.test(baseAnalysis.ocrText),
    hasContactForm: baseAnalysis.ocrText.includes('お問い合わせ') || 
                    baseAnalysis.ocrText.includes('連絡先'),
    systemAnalysis: analyzeSystemElements(baseAnalysis.ocrText)
  };
  
  return kinkamasuAnalysis;
}

/**
 * システム要素を分析
 * @param {string} ocrText - OCRテキスト
 * @return {Object} システム分析結果
 */
function analyzeSystemElements(ocrText) {
  return {
    hasWordPress: ocrText.includes('WordPress') || ocrText.includes('wp-'),
    hasDatabase: ocrText.includes('MySQL') || ocrText.includes('データベース'),
    hasAPI: ocrText.includes('API') || ocrText.includes('JSON'),
    hasSSL: ocrText.includes('https://') || ocrText.includes('SSL'),
    needsImprovement: identifyImprovementAreas(ocrText)
  };
}

/**
 * 改善が必要な領域を特定
 * @param {string} ocrText - OCRテキスト
 * @return {Array} 改善提案リスト
 */
function identifyImprovementAreas(ocrText) {
  const improvements = [];
  
  if (!ocrText.includes('レスポンシブ')) {
    improvements.push('モバイル対応の改善');
  }
  
  if (!ocrText.includes('SSL') && !ocrText.includes('https://')) {
    improvements.push('SSL証明書の導入');
  }
  
  if (ocrText.includes('エラー') || ocrText.includes('Error')) {
    improvements.push('エラーハンドリングの改善');
  }
  
  return improvements;
}
